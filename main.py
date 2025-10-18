import sys

def normalize(word):
    if word is None:
        return ""
    w = word.strip().lower()

    accented = [
        'á','à','ä','â','ã','å',
        'é','è','ë','ê',
        'í','ì','ï','î',
        'ó','ò','ö','ô','õ',
        'ú','ù','ü','û',
        'ç'
    ]
    repl = [
        'a','a','a','a','a','a',
        'e','e','e','e',
        'i','i','i','i',
        'o','o','o','o','o',
        'u','u','u','u',
        'c'
    ]

    res_chars = []
    for ch in w:
        if ch == 'ñ':
            res_chars.append('ñ')
        else:
            if ch in accented:
                idx = accented.index(ch)
                res_chars.append(repl[idx])
            else:
                res_chars.append(ch)
    return ''.join(res_chars)


def leer_diccionario(path):
    entradas = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                if ":" not in linea:
                    continue
                palabra_raw, freq_raw = linea.split(":", 1)
                palabra_raw = palabra_raw.strip().strip("'\"")
                freq_raw = freq_raw.strip().rstrip(",")
                palabra = normalize(palabra_raw)
                try:
                    freq = int(freq_raw)
                except:
                    continue
                entradas.append((palabra, freq))
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{path}'.")
        return []

    entradas.sort(key=lambda x: x[0])

    combinadas = []
    for w, f in entradas:
        if not combinadas:
            combinadas.append((w, f))
        else:
            if combinadas[-1][0] == w:
                prev_f = combinadas[-1][1]
                if f > prev_f:
                    combinadas[-1] = (w, f)
            else:
                combinadas.append((w, f))

    return combinadas


def binaria_tuplas(dicc, objetivo):
    izquierda = 0
    derecha = len(dicc) - 1
    while izquierda <= derecha:
        mid = (izquierda + derecha) // 2
        mid_word = dicc[mid][0]
        if mid_word == objetivo:
            return mid
        elif mid_word < objetivo:
            izquierda = mid + 1
        else:
            derecha = mid - 1
    return -1


def generar_variantes_1ed(w, alfabeto):
    variantes = []
    n = len(w)

    for i in range(n):
        variantes.append(w[:i] + w[i+1:])

    for i in range(n + 1):
        for c in alfabeto:
            variantes.append(w[:i] + c + w[i:])

    for i in range(n):
        for c in alfabeto:
            if c != w[i]:
                variantes.append(w[:i] + c + w[i+1:])

    for i in range(n - 1):
        variantes.append(w[:i] + w[i+1] + w[i] + w[i+2:])

    return variantes


def filtrar_contra_dicc(variantes, dicc):
    candidatos = []
    for v in variantes:
        idx = binaria_tuplas(dicc, v)
        if idx != -1:
            candidatos.append(dicc[idx])
    return candidatos


def deduplicar_ordenado(cands):
    if not cands:
        return []

    cands.sort(key=lambda x: x[0])
    res = []
    i = 0
    n = len(cands)
    while i < n:
        w = cands[i][0]
        maxf = cands[i][1]
        j = i + 1
        while j < n and cands[j][0] == w:
            if cands[j][1] > maxf:
                maxf = cands[j][1]
            j += 1
        res.append((w, maxf))
        i = j
    return res


def ordenar_por_frecuencia(cands):
    return sorted(cands, key=lambda x: (-x[1], x[0]))


def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py palabra k")
        print("Ejemplo: python main.py çassa 3")
        return

    palabra_input = sys.argv[1]
    try:
        k = int(sys.argv[2])
        if k <= 0:
            raise ValueError()
    except:
        print("Error: 'k' debe ser un entero positivo.")
        return

    alfabeto = list("abcdefghijklmnopqrstuvwxyzñ")
    dicc = leer_diccionario("word_freq.txt")
    if not dicc:
        print("Diccionario vacío o no encontrado.")
        return

    palabra = normalize(palabra_input)
    idx = binaria_tuplas(dicc, palabra)
    if idx != -1:
        encontrado = dicc[idx]
        print(f"Palabra encontrada: {encontrado[0]} (freq={encontrado[1]})")
        return

    variantes = generar_variantes_1ed(palabra, alfabeto)
    candidatos = filtrar_contra_dicc(variantes, dicc)
    candidatos = deduplicar_ordenado(candidatos)
    candidatos = ordenar_por_frecuencia(candidatos)

    if not candidatos:
        print(f"No se encontraron sugerencias para '{palabra_input}'.")
        return

    print(f"Sugerencias Top-{k} para '{palabra_input}':")
    to_show = candidatos[:k]
    for i, (w, f) in enumerate(to_show, start=1):
        print(f"{i}. {w} (freq={f})")


if __name__ == "__main__":  # pragma: no cover
    main()
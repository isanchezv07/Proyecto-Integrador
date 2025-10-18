# Proyecto Integrador

Un corrector ortográfico simple e inteligente construido con Python que sugiere correcciones basadas en un diccionario de palabras con frecuencias.

---

## ✨ Características

- **Normalización Inteligente**: Elimina acentos y caracteres especiales (`áéíóú` → `aeiou`, `ç` → `c`), conservando `ñ`
- **Diccionario con Frecuencias**: Lee y procesa un diccionario de palabras con su frecuencia de uso
- **Búsqueda Eficiente**: Utiliza búsqueda binaria para encontrar coincidencias exactas
- **Sugerencias Inteligentes**: Genera variantes a una edición de distancia (inserción, eliminación, sustitución, transposición)
- **Ordenamiento Optimizado**: Ordena sugerencias por frecuencia y alfabéticamente

---

## 📋 Requisitos

- Python 3.8 o superior
- Archivo `word_freq.txt` en formato UTF-8

### Formato del Diccionario

```txt
'palabra': frecuencia,
'otra': 12,
'ejemplo': 456,
```

---

## 🚀 Uso

### Ejecución Básica

```bash
python main.py palabra k
```

**Parámetros:**
- `palabra`: Palabra a verificar o corregir
- `k`: Número máximo de sugerencias a mostrar (entero positivo)

### Ejemplo Práctico

```bash
python main.py hte 3
```

**Salida:**
```
Sugerencias Top-3 para 'hte':
1. the (freq=79809)
2. he (freq=12401)
3. ate (freq=21)
```

---

## 📁 Estructura del Proyecto

```
PROYECTO/
│
├── main.py              # Código principal del corrector
├── word_freq.txt        # Diccionario de palabras y frecuencias
└── tests/
    └── test_sample.py   # Pruebas unitarias
```

---

## 🔧 Funciones Principales

### `normalize(word)`
Normaliza una palabra eliminando espacios, acentos y caracteres especiales.

### `leer_diccionario(path)`
Lee el diccionario y combina duplicados, manteniendo la frecuencia más alta.

### `binaria_tuplas(dicc, objetivo)`
Busca una palabra en el diccionario usando búsqueda binaria.

### `generar_variantes_1ed(w, alfabeto)`
Genera variantes a una edición de distancia mediante:
- Inserción de caracteres
- Eliminación de caracteres
- Sustitución de caracteres
- Transposición de letras adyacentes

### `filtrar_contra_dicc(variantes, dicc)`
Filtra variantes que existen en el diccionario.

### `deduplicar_ordenado(cands)`
Elimina duplicados manteniendo la mayor frecuencia.

### `ordenar_por_frecuencia(cands)`
Ordena descendentemente por frecuencia y alfabéticamente.

---

## 🧪 Pruebas

### Ejecutar Tests con Cobertura

```bash
pytest --cov=main --cov-report=term-missing
```

**Parámetros:**
- `--cov=main`: Mide cobertura del archivo `main.py`
- `--cov-report=term-missing`: Muestra líneas no ejecutadas

### Cobertura Completa del Proyecto

```bash
pytest -q --cov=. --cov-report=term-missing
```

---

## 💡 Algoritmo

El corrector utiliza un enfoque basado en:

1. **Normalización** de entrada
2. **Búsqueda exacta** en el diccionario
3. **Generación de variantes** a una edición de distancia
4. **Filtrado** contra el diccionario
5. **Ordenamiento** por relevancia (frecuencia + alfabético)

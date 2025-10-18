#IsanchezV07-17/10/2025
import builtins
import tempfile
import io
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import main, leer_diccionario

# ------------------- Tests de leer_diccionario -------------------

def test_leer_diccionario_no_file():
    resultado = leer_diccionario("no_existe.txt")
    assert resultado == []

def test_leer_diccionario_lineas_invalidas(tmp_path):
    f = tmp_path / "dicc.txt"
    f.write_text("'hola': 10,\n'invalido'\n'mal': x,\n'a': 1,\n'a': 5,\n")
    resultado = leer_diccionario(str(f))
    assert resultado == [("a", 5), ("hola", 10)]

# ------------------- Tests de main() -------------------

def test_main_no_args(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    main()
    out = capsys.readouterr().out
    assert "Uso" in out

def test_main_k_invalido(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "hola", "0"])
    main()
    out = capsys.readouterr().out
    assert "Error" in out

def test_main_dicc_vacio(monkeypatch, capsys, tmp_path):
    f = tmp_path / "word_freq.txt"
    f.write_text("", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["main.py", "hola", "3"])
    os.chdir(tmp_path)
    main()
    out = capsys.readouterr().out
    assert "Diccionario vacío" in out

def test_main_archivo_no_existe(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(sys, "argv", ["main.py", "hola", "3"])
    os.chdir(tmp_path)  
    main()
    out = capsys.readouterr().out
    assert "Diccionario vacío" in out or "no se encontró" in out.lower()

def test_main_palabra_encontrada(monkeypatch, capsys, tmp_path):
    f = tmp_path / "word_freq.txt"
    f.write_text("'hola': 10,", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["main.py", "hola", "3"])
    os.chdir(tmp_path)
    main()
    out = capsys.readouterr().out
    assert "Palabra encontrada" in out

def test_main_sin_sugerencias(monkeypatch, capsys, tmp_path):
    f = tmp_path / "word_freq.txt"
    f.write_text("'hola': 10,", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["main.py", "zzz", "3"])  
    os.chdir(tmp_path)
    main()
    out = capsys.readouterr().out
    assert "No se encontraron" in out

def test_main_con_sugerencias(monkeypatch, capsys, tmp_path):
    f = tmp_path / "word_freq.txt"
    f.write_text("'hola': 10,\n'hila': 8,\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["main.py", "holb", "2"])
    os.chdir(tmp_path)
    main()
    out = capsys.readouterr().out
    assert "Sugerencias" in out

# ------------------- Test bloque principal -------------------

def test_run_directamente():
    import importlib
    import main
    importlib.reload(main)  
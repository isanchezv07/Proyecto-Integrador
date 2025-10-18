# 🧩 Cómo correr el codigo

1. Ejecutar el comando desde la terminal

> La palabra que pongas tiene que ser en ingles

```bash
python3 main.py <palabra> <k>
```

correr los test y ver si pasaron
```bash
pytest -v
```

correr los test de coverage del main
```bash
coverage run main.py  hte 10
```

ver los coverage de los test
```bash
coverage report -m
```
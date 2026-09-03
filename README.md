# AUTOMATIK CR

Página web inicial para AUTOMATIK CR, lista para subir a GitHub y desplegar en Render.

## Estructura

- app.py
- requirements.txt
- render.yaml
- templates/index.html
- static/css/style.css

## GitHub

1. Crear un repositorio nuevo.
2. Subir todos los archivos y carpetas conservando la estructura.
3. Hacer commit.

## Render

1. New + → Web Service.
2. Conectar el repositorio de GitHub.
3. Runtime: Python.
4. Build Command:
   pip install -r requirements.txt
5. Start Command:
   gunicorn app:app --bind 0.0.0.0:$PORT
6. Deploy Web Service.

Render también puede detectar el archivo render.yaml.


# AUTOMATIK CR — Web V2 Avanzada

Versión avanzada de la página de AUTOMATIK CR, lista para GitHub + Render.

## Incluye

- Página principal premium y responsive.
- Hero tecnológico con imagen de marca.
- Servicios: bots, IA, páginas web, automatización, correos y dashboards.
- Sección "Soluciones por industria".
- Páginas individuales para:
  - Restaurantes
  - Comercios
  - Oficinas
  - Finanzas y fiduciarias
  - Construcción e ingeniería
  - Turismo y hotelería
  - Educación
  - Pymes y emprendedores
- Demo interactivo de restaurante:
  - agrega productos,
  - calcula el total,
  - envía el pedido,
  - muestra la orden en cocina,
  - cambia el estado del pedido.
- Botones directos a WhatsApp.
- Correo y web corporativos.
- Animaciones al hacer scroll.
- Diseño responsive para computadora y celular.

## Datos actuales

- WhatsApp: +506 7164 2558
- Correo: automatikcr@outlook.es
- Web actual: https://automatik-cr.onrender.com/

## Cómo actualizar GitHub

Puedes reemplazar los archivos actuales del repositorio `automatik-cr` con el contenido de esta carpeta.

Estructura principal:

app.py
requirements.txt
render.yaml
templates/
static/

No subas la carpeta exterior si quieres que `app.py` quede en la raíz del repositorio.

## Render

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app --bind 0.0.0.0:$PORT

Si el servicio de Render ya está conectado al repositorio y tiene Auto-Deploy activo, al hacer commit de estos archivos Render debería desplegar automáticamente la nueva versión.

## Próximas mejoras posibles

- Formulario real conectado a correo.
- CRM de contactos.
- Cotizador.
- Blog.
- Panel de clientes.
- Login.
- Base de datos.
- Integración con WhatsApp API.
- Chatbot IA.
- Dominio propio automatik.cr.

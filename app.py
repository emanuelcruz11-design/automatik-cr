
from flask import Flask, render_template

app = Flask(__name__)

INDUSTRIES = [
    {
        "slug": "restaurantes",
        "name": "Restaurantes",
        "icon": "🍽️",
        "tagline": "Menú, pedidos, cocina y control en un solo flujo.",
        "problems": ["Pedidos manuales y errores de digitación", "Demoras entre salón y cocina", "Poca visibilidad del estado de cada orden"],
        "solutions": ["Menú digital", "Pedidos por mesa o para llevar", "Panel de cocina", "Estados del pedido", "Reportes de ventas"]
    },
    {
        "slug": "comercios",
        "name": "Comercios",
        "icon": "🛍️",
        "tagline": "Ventas, consultas y seguimiento con menos trabajo manual.",
        "problems": ["Consultas repetitivas", "Cotizaciones manuales", "Seguimiento disperso"],
        "solutions": ["Catálogo web", "Bots de atención", "Cotizaciones automáticas", "Seguimiento comercial", "Reportes"]
    },
    {
        "slug": "oficinas",
        "name": "Oficinas",
        "icon": "🏢",
        "tagline": "Procesos administrativos más ágiles y trazables.",
        "problems": ["Correos repetitivos", "Documentos manuales", "Información en múltiples archivos"],
        "solutions": ["Automatización de correos", "Generación de documentos", "Formularios", "Dashboards", "Flujos de aprobación"]
    },
    {
        "slug": "finanzas",
        "name": "Finanzas y fiduciarias",
        "icon": "🏦",
        "tagline": "Conciliaciones, consultas, reportes y controles automatizados.",
        "problems": ["Altos volúmenes de datos", "Conciliaciones manuales", "Seguimientos periódicos"],
        "solutions": ["Bots de consulta", "Conciliaciones automáticas", "Alertas", "Reportes ejecutivos", "Correos masivos con adjuntos"]
    },
    {
        "slug": "construccion",
        "name": "Construcción e ingeniería",
        "icon": "🏗️",
        "tagline": "Control de obra y reportes con información más clara.",
        "problems": ["Seguimiento manual de avances", "Reportes dispersos", "Control de costos y actividades"],
        "solutions": ["Dashboards de obra", "Formularios de campo", "Control de avances", "Reportes automáticos", "Portales de proyecto"]
    },
    {
        "slug": "turismo",
        "name": "Turismo y hotelería",
        "icon": "🏨",
        "tagline": "Atención, reservas y seguimiento de huéspedes.",
        "problems": ["Consultas frecuentes", "Procesos de reserva manuales", "Seguimiento fragmentado"],
        "solutions": ["Bots de atención", "Formularios de reserva", "Recordatorios", "Guías digitales", "Paneles de seguimiento"]
    },
    {
        "slug": "educacion",
        "name": "Educación",
        "icon": "🎓",
        "tagline": "Comunicación y procesos académicos más eficientes.",
        "problems": ["Consultas repetitivas", "Seguimientos manuales", "Información dispersa"],
        "solutions": ["Bots de información", "Formularios", "Recordatorios", "Portales informativos", "Reportes"]
    },
    {
        "slug": "pymes",
        "name": "Pymes y emprendedores",
        "icon": "🚀",
        "tagline": "Tecnología práctica para crecer sin complicarse.",
        "problems": ["Procesos manuales", "Poca presencia digital", "Seguimiento comercial limitado"],
        "solutions": ["Página web", "WhatsApp y formularios", "Automatizaciones", "Cotizaciones", "Reportes básicos"]
    }
]

@app.route("/")
def home():
    return render_template("index.html", industries=INDUSTRIES)

@app.route("/soluciones/<slug>")
def industry(slug):
    item = next((x for x in INDUSTRIES if x["slug"] == slug), None)
    if not item:
        return render_template("404.html"), 404
    return render_template("industry.html", item=item, industries=INDUSTRIES)

@app.route("/demo-restaurante")
def restaurant_demo():
    return render_template("restaurant_demo.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from io import BytesIO
import threading
import qrcode
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage

app = Flask(__name__)

INDUSTRIES = [
    {"slug":"restaurantes","name":"Restaurantes","icon":"🍽️","tagline":"Menú, pedidos, cocina y control en un solo flujo.","problems":["Pedidos manuales y errores de digitación","Demoras entre salón y cocina","Poca visibilidad del estado de cada orden"],"solutions":["Menú digital","Pedidos por mesa o para llevar","Panel de cocina","Estados del pedido","Reportes de ventas"],"examples":["Pedido digital que llega directo a cocina","Avisos de estado para salón o cliente","Reporte de productos más vendidos"]},
    {"slug":"comercios","name":"Comercios","icon":"🛍️","tagline":"Ventas, consultas y seguimiento con menos trabajo manual.","problems":["Consultas repetitivas","Cotizaciones manuales","Seguimiento disperso"],"solutions":["Catálogo web","Bots de atención","Cotizaciones automáticas","Seguimiento comercial","Reportes"],"examples":["Formulario que registra oportunidades","Respuestas automáticas a preguntas frecuentes","Seguimiento de cotizaciones y clientes"]},
    {"slug":"oficinas","name":"Oficinas","icon":"🏢","tagline":"Procesos administrativos más ágiles y trazables.","problems":["Correos repetitivos","Documentos manuales","Información en múltiples archivos"],"solutions":["Automatización de correos","Generación de documentos","Formularios","Dashboards","Flujos de aprobación"],"examples":["Envíos masivos con documentos personalizados","Consolidación de datos en reportes","Alertas y seguimiento de tareas"]},
    {"slug":"finanzas","name":"Finanzas y fiduciarias","icon":"🏦","tagline":"Conciliaciones, consultas, reportes y controles automatizados.","problems":["Altos volúmenes de datos","Conciliaciones manuales","Seguimientos periódicos"],"solutions":["Bots de consulta","Conciliaciones automáticas","Alertas","Reportes ejecutivos","Correos masivos con adjuntos"],"examples":["Consulta masiva de información","Cruce y validación de bases","Generación y distribución de reportes"]},
    {"slug":"construccion","name":"Construcción e ingeniería","icon":"🏗️","tagline":"Control de obra y reportes con información más clara.","problems":["Seguimiento manual de avances","Reportes dispersos","Control de costos y actividades"],"solutions":["Dashboards de obra","Formularios de campo","Control de avances","Reportes automáticos","Portales de proyecto"],"examples":["Registro de avances desde campo","Panel de proyectos, responsables y estados","Gestión de usuarios y acceso por proyecto"]},
    {"slug":"turismo","name":"Turismo y hotelería","icon":"🏨️","tagline":"Atención, reservas y seguimiento de huéspedes.","problems":["Consultas frecuentes","Procesos de reserva manuales","Seguimiento fragmentado"],"solutions":["Bots de atención","Formularios de reserva","Recordatorios","Guías digitales","Paneles de seguimiento"],"examples":["Captura automática de solicitudes","Confirmaciones y recordatorios","Panel de reservas y seguimiento"]},
    {"slug":"educacion","name":"Educación","icon":"🎓","tagline":"Comunicación y procesos académicos más eficientes.","problems":["Consultas repetitivas","Seguimientos manuales","Información dispersa"],"solutions":["Bots de información","Formularios","Recordatorios","Portales informativos","Reportes"],"examples":["Inscripciones y solicitudes digitales","Recordatorios automáticos","Reportes de seguimiento"]},
    {"slug":"pymes","name":"Pymes y emprendedores","icon":"🚀","tagline":"Tecnología práctica para crecer sin complicarse.","problems":["Procesos manuales","Poca presencia digital","Seguimiento comercial limitado"],"solutions":["Página web","WhatsApp y formularios","Automatizaciones","Cotizaciones","Reportes básicos"],"examples":["Sitio web con contacto directo","Registro de prospectos","Automatización de tareas administrativas"]}
]

RESTAURANT = {
    "name": "Brasa Urbana",
    "subtitle": "Kitchen & Grill",
    "currency": "₡",
    "service_note": "Demo interactiva desarrollada por AUTOMATIK CR",
}

MENU = [
    {"id":1,"category":"Entradas","name":"Patacones Brasa","desc":"Patacones crujientes, frijoles molidos, pico de gallo y crema de la casa.","price":3900,"image":"https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=80","tags":["Popular"]},
    {"id":2,"category":"Entradas","name":"Camarones Crispy","desc":"Camarones empanizados con salsa cítrica ligeramente picante.","price":5900,"image":"https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=900&q=80","tags":["Picante"]},
    {"id":3,"category":"Entradas","name":"Croquetas de Pollo","desc":"Seis croquetas doradas con alioli de ajo rostizado.","price":4200,"image":"https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?auto=format&fit=crop&w=900&q=80","tags":[]},
    {"id":4,"category":"Hamburguesas","name":"Brasa Classic","desc":"Carne 150 g, queso, lechuga, tomate, cebolla caramelizada y salsa Brasa.","price":6900,"image":"https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=80","tags":["Más vendido"]},
    {"id":5,"category":"Hamburguesas","name":"BBQ Bacon","desc":"Carne 150 g, cheddar, bacon crocante, cebolla crispy y BBQ ahumada.","price":7900,"image":"https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=900&q=80","tags":["Popular"]},
    {"id":6,"category":"Hamburguesas","name":"Crispy Chicken","desc":"Pollo crujiente, repollo fresco, pepinillos y mayonesa de limón.","price":6500,"image":"https://images.unsplash.com/photo-1615297928064-24977384d0da?auto=format&fit=crop&w=900&q=80","tags":[]},
    {"id":7,"category":"Platos fuertes","name":"Pollo al Grill","desc":"Pechuga marinada, vegetales salteados y papas rústicas.","price":7600,"image":"https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=900&q=80","tags":["Sin gluten"]},
    {"id":8,"category":"Platos fuertes","name":"Salmón Glaseado","desc":"Salmón a la plancha con glaseado cítrico, arroz jazmín y vegetales.","price":9900,"image":"https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=900&q=80","tags":["Chef recomienda"]},
    {"id":9,"category":"Platos fuertes","name":"Pasta Cremosa","desc":"Pasta al dente con pollo, hongos, parmesano y salsa cremosa.","price":7200,"image":"https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=80","tags":[]},
    {"id":10,"category":"Bowls & Ensaladas","name":"Tropical Bowl","desc":"Arroz, aguacate, mango, maíz, edamame, repollo y aderezo cítrico.","price":6100,"image":"https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80","tags":["Vegetariano"]},
    {"id":11,"category":"Bowls & Ensaladas","name":"Chicken Bowl","desc":"Pollo grill, arroz, frijoles, pico de gallo, aguacate y maíz dulce.","price":6900,"image":"https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80","tags":[]},
    {"id":12,"category":"Bebidas","name":"Limonada Hierbabuena","desc":"Limón recién exprimido con hierbabuena y hielo.","price":2200,"image":"https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=900&q=80","tags":["Refrescante"]},
    {"id":13,"category":"Bebidas","name":"Té Frío Tropical","desc":"Té negro frío con maracuyá y naranja.","price":2400,"image":"https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=80","tags":[]},
    {"id":14,"category":"Bebidas","name":"Café Americano","desc":"Café de altura costarricense.","price":1800,"image":"https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=80","tags":[]},
    {"id":15,"category":"Postres","name":"Brownie Caliente","desc":"Brownie tibio de chocolate con helado de vainilla.","price":3600,"image":"https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80","tags":["Favorito"]},
    {"id":16,"category":"Postres","name":"Cheesecake de Maracuyá","desc":"Cheesecake cremoso con cobertura de maracuyá.","price":3900,"image":"https://images.unsplash.com/photo-1524351199678-941a58a3df50?auto=format&fit=crop&w=900&q=80","tags":[]}
]

ORDERS = []
LOCK = threading.Lock()
STATUS_FLOW = ["Pendiente de pago", "Recibido", "En preparación", "Listo", "Entregado"]
CR_TZ = ZoneInfo("America/Costa_Rica")
DEFAULT_ESTIMATED_MINUTES = 25
IVA_RATE = 0.13

def now_cr():
    return datetime.now(CR_TZ)

def time_label(dt):
    return dt.strftime("%H:%M")

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
    # Entrada única de la demostración: siempre inicia desde la experiencia del cliente.
    categories = list(dict.fromkeys(item["category"] for item in MENU))
    return render_template("restaurant_menu.html", restaurant=RESTAURANT, menu=MENU, categories=categories, mesa=7, guided_demo=True)

@app.route("/demo-restaurante/menu/<int:mesa>")
def restaurant_menu(mesa):
    categories = list(dict.fromkeys(item["category"] for item in MENU))
    return render_template("restaurant_menu.html", restaurant=RESTAURANT, menu=MENU, categories=categories, mesa=mesa)

@app.route("/demo-restaurante/cocina")
def restaurant_kitchen():
    return render_template("restaurant_kitchen.html", restaurant=RESTAURANT, statuses=STATUS_FLOW)

@app.route("/demo-restaurante/admin")
def restaurant_admin():
    return render_template("restaurant_admin.html", restaurant=RESTAURANT)

@app.route("/demo-restaurante/qr")
def restaurant_qr_hub():
    return render_template("restaurant_qr_hub.html", restaurant=RESTAURANT, mesas=range(1, 13))

@app.route("/demo-restaurante/qr/<int:mesa>.png")
def restaurant_qr(mesa):
    url = request.url_root.rstrip("/") + f"/demo-restaurante/menu/{mesa}"
    img = qrcode.make(url)
    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return send_file(bio, mimetype="image/png", download_name=f"mesa-{mesa}.png")

@app.route("/api/restaurant/orders", methods=["GET", "POST"])
def orders_api():
    if request.method == "POST":
        data = request.get_json(force=True)
        items = data.get("items", [])
        if not items:
            return jsonify({"error": "El pedido no contiene productos."}), 400
        with LOCK:
            order_id = f"BU-{1000 + len(ORDERS) + 1}"
            created = now_cr()
            estimated = created + timedelta(minutes=DEFAULT_ESTIMATED_MINUTES)
            order = {
                "id": order_id,
                "mesa": data.get("mesa"),
                "customer": data.get("customer", "Cliente"),
                "notes": data.get("notes", ""),
                "items": items,
                "total": data.get("total", 0),
                "status": "Pendiente de pago",
                "payment_status": "Pendiente",
                "estimated_minutes": DEFAULT_ESTIMATED_MINUTES,
                "created_at": time_label(created),
                "created_iso": created.isoformat(timespec="seconds"),
                "started_at": time_label(created),
                "prep_started_at": None,
                "ready_at": None,
                "delivered_at": None,
                "paid_at": None,
                "finished_at": None,
                "estimated_delivery_at": time_label(estimated),
                "status_history": [{"status": "Pendiente de pago", "time": time_label(created)}],
                "invoice_number": None,
                "payment_method": None
            }
            ORDERS.insert(0, order)
        return jsonify(order), 201
    return jsonify(ORDERS)

@app.route("/api/restaurant/orders/<order_id>", methods=["GET", "PATCH"])
def order_detail(order_id):
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404
    if request.method == "PATCH":
        data = request.get_json(force=True)
        status = data.get("status")
        if status in STATUS_FLOW and status != order.get("status"):
            stamp = now_cr()
            label = time_label(stamp)

            # El cliente debe pagar antes de que cocina reciba la orden.
            if order.get("status") == "Pendiente de pago" and status != "Recibido":
                return jsonify({"error": "Primero debe pagarse el pedido."}), 409

            if status == "Recibido" and order.get("status") == "Pendiente de pago":
                order["payment_status"] = "Pagado"
                order["paid_at"] = label
                order["payment_method"] = data.get("payment_method", "Tarjeta demo")
                if not order.get("invoice_number"):
                    order["invoice_number"] = f"FAC-DEMO-{1000 + len([o for o in ORDERS if o.get('invoice_number')]) + 1}"

            order["status"] = status
            order.setdefault("status_history", []).append({"status": status, "time": label})
            if status == "En preparación" and not order.get("prep_started_at"):
                order["prep_started_at"] = label
            elif status == "Listo" and not order.get("ready_at"):
                order["ready_at"] = label
            elif status == "Entregado" and not order.get("delivered_at"):
                order["delivered_at"] = label
                order["finished_at"] = label
        return jsonify(order)
    return jsonify(order)


@app.route("/demo-restaurante/factura/<order_id>.pdf")
def restaurant_invoice(order_id):
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404
    if order.get("payment_status") != "Pagado":
        return jsonify({"error": "La factura demo se genera cuando el cliente paga el pedido."}), 409

    invoice_number = order.get("invoice_number") or f"FAC-DEMO-{order_id.replace('BU-', '')}"
    order["invoice_number"] = invoice_number
    total = float(order.get("total", 0) or 0)
    subtotal = round(total / (1 + IVA_RATE), 2) if total else 0
    iva = round(total - subtotal, 2)

    qr_url = request.url_root.rstrip("/") + f"/api/restaurant/orders/{order_id}"
    qr_img = qrcode.make(qr_url)
    qr_bio = BytesIO()
    qr_img.save(qr_bio, format="PNG")
    qr_bio.seek(0)

    pdf = BytesIO()
    doc = SimpleDocTemplate(pdf, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
    styles = getSampleStyleSheet()
    title = ParagraphStyle('InvoiceTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=colors.HexColor('#171411'))
    orange = ParagraphStyle('Orange', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#F06B21'), spaceAfter=4)
    small = ParagraphStyle('Small', parent=styles['Normal'], fontSize=8.5, leading=12, textColor=colors.HexColor('#625B55'))
    right = ParagraphStyle('Right', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=9, leading=13)
    center = ParagraphStyle('Center', parent=small, alignment=TA_CENTER)

    story = []
    header = Table([[
        [Paragraph('BRASA URBANA', title), Paragraph('KITCHEN & GRILL', orange), Paragraph('Comprobante demostrativo', small)],
        [Paragraph(f'<b>{invoice_number}</b>', right), Paragraph(f'Pedido: {order_id}', right), Paragraph(f'Mesa: {order.get("mesa", "-")}', right)]
    ]], colWidths=[105*mm, 65*mm])
    header.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),0.8,colors.HexColor('#EADFD4')),('BOTTOMPADDING',(0,0),(-1,0),8)]))
    story += [header, Spacer(1, 8*mm)]

    info = Table([
        ['Cliente', order.get('customer') or 'Cliente'],
        ['Hora de inicio', order.get('started_at') or order.get('created_at') or '--:--'],
        ['Hora de pago', order.get('paid_at') or '--:--'],
        ['Método de pago', order.get('payment_method') or 'Tarjeta demo'],
        ['Estado', 'PAGADO']
    ], colWidths=[42*mm, 128*mm])
    info.setStyle(TableStyle([('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTNAME',(1,0),(1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),9),('TEXTCOLOR',(0,0),(0,-1),colors.HexColor('#746D66')),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story += [info, Spacer(1, 6*mm)]

    rows = [['Cant.', 'Producto', 'Precio unit.', 'Total']]
    for item in order.get('items', []):
        qty = int(item.get('qty', 1) or 1)
        price = float(item.get('price', 0) or 0)
        rows.append([str(qty), item.get('name','Producto'), f'CRC {price:,.0f}', f'CRC {price*qty:,.0f}'])
    item_table = Table(rows, colWidths=[18*mm, 92*mm, 30*mm, 30*mm], repeatRows=1)
    item_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#171411')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('ALIGN',(0,0),(0,-1),'CENTER'),('ALIGN',(2,1),(-1,-1),'RIGHT'),('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#EADFD4')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#FFF8F1')]),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)
    ]))
    story += [item_table, Spacer(1, 6*mm)]

    totals = Table([
        ['Subtotal', f'CRC {subtotal:,.2f}'],
        ['IVA demo 13%', f'CRC {iva:,.2f}'],
        ['TOTAL', f'CRC {total:,.2f}']
    ], colWidths=[120*mm, 50*mm])
    totals.setStyle(TableStyle([('ALIGN',(1,0),(1,-1),'RIGHT'),('FONTNAME',(0,0),(-1,-2),'Helvetica'),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-2),10),('FONTSIZE',(0,-1),(-1,-1),13),('LINEABOVE',(0,-1),(-1,-1),1.2,colors.HexColor('#F06B21')),('TOPPADDING',(0,-1),(-1,-1),8)]))
    story += [totals, Spacer(1, 8*mm)]

    if order.get('notes'):
        story += [Paragraph('<b>Observaciones del pedido</b>', small), Paragraph(order.get('notes'), small), Spacer(1, 5*mm)]

    qr = RLImage(qr_bio, width=28*mm, height=28*mm)
    footer = Table([[qr, Paragraph('<b>DEMO AUTOMATIK CR</b><br/>Este documento es una simulación para demostrar el flujo de un sistema de restaurante. No es una factura electrónica ni tiene validez fiscal.<br/><br/>Automatización · Web · Bots · Publicidad Digital', center)]], colWidths=[34*mm,136*mm])
    footer.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('BOX',(0,0),(-1,-1),0.6,colors.HexColor('#EADFD4')),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FFF8F1')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    story.append(footer)

    doc.build(story)
    pdf.seek(0)
    return send_file(pdf, mimetype='application/pdf', as_attachment=False, download_name=f'{invoice_number}.pdf')

@app.route("/api/restaurant/reset", methods=["POST"])
def reset_demo():
    with LOCK:
        ORDERS.clear()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

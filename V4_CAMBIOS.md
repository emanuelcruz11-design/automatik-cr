# AUTOMATIK CR V4 — Demo Restaurante QR

## Novedades
- Restaurante ficticio: **Brasa Urbana · Kitchen & Grill**.
- QR real por mesa (`/demo-restaurante/qr/<mesa>.png`).
- Menú visual responsive con 16 productos genéricos, categorías, buscador, fotos y precios ficticios.
- Carrito, cantidades, nombre del cliente y observaciones.
- Envío del pedido a una API Flask en memoria.
- Seguimiento del pedido: Recibido → En preparación → Listo → Entregado → Pagado.
- Panel de cocina en `/demo-restaurante/cocina`.
- Panel administrativo en `/demo-restaurante/admin`.
- Botón para reiniciar la demo.

## Nota técnica
Los pedidos se guardan **en memoria** para fines de demostración. Si Render reinicia el servicio, los pedidos se borran. Para producción conviene usar PostgreSQL y autenticación por roles.

## Corrección visual 08-09-2026
- Corregido el bloque “Soluciones por industria” que aparecía con fondo blanco por una colisión de la clase CSS `.light`.
- El estilo blanco queda limitado a botones (`.btn.light`) y el encabezado oscuro usa `.section-head.light` con fondo transparente.

## Publicidad digital
- Nuevo servicio “Publicidad digital” en la página principal.
- Incluye campañas para Facebook e Instagram, piezas, landing pages, WhatsApp y seguimiento de prospectos.
- Nuevo caso de uso “Publicidad + embudo comercial”.
- Nuevo campo “Servicio de interés” en el formulario de cotización.
- El mensaje de WhatsApp ahora incluye el servicio seleccionado.
- Metadatos y portada actualizados para incorporar publicidad digital.

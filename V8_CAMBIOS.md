# V8 · Pago previo a cocina

- El pedido nace en estado **Pendiente de pago**.
- El cliente selecciona un método de pago demo y debe pagar antes de que cocina reciba la orden.
- Al aprobarse el pago, el pedido cambia automáticamente a **Recibido** y aparece en Cocina.
- Cocina solo muestra pedidos pagados y maneja el flujo: **Recibido → En preparación → Listo → Entregado**.
- Se genera la factura PDF desde el momento en que el pago queda aprobado.
- Administración conserva visibilidad de pedidos pendientes de pago y pagados.
- La vista Cliente muestra claramente el paso de pago y confirma cuándo el pedido fue enviado a Cocina.

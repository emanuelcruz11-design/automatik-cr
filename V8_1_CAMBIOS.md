# V8.1 - Corrección factura en Administración

- La columna Factura ahora valida `payment_status == Pagado` en lugar del estado operativo del pedido.
- La factura PDF permanece disponible aunque el pedido esté en estado Recibido, En preparación, Listo o Entregado.

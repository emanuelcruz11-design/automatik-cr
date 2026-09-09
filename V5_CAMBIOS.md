# AUTOMATIK CR V5 · Demo Restaurante 360

## Mejoras principales
- Nuevo Centro de Demostración con acceso visible a Cliente, QR, Cocina y Administración.
- Navegación entre módulos sin necesidad de conocer URLs técnicas.
- Comportamiento adaptativo: en computadora se muestra QR; en móvil se prioriza el botón de prueba directa.
- Galería de QR para 12 mesas.
- Hora de inicio del pedido.
- Hora estimada de entrega (25 minutos en la demo).
- Hora de fin cuando el pedido se marca como Entregado.
- Hora de pago cuando se completa el flujo.
- Historial de estados en la API.
- Panel de cocina con tiempos visibles por orden.
- Panel administrativo con inicio, estimada, fin y duración.
- En la confirmación del cliente aparecen los tiempos y accesos directos a Cocina y Administración.

## Flujo de prueba
Cliente → Pedido → Cocina → En preparación → Listo → Entregado → Pago → Administración.

## Nota técnica
Los pedidos continúan en memoria para fines de demostración. Para producción se recomienda PostgreSQL y autenticación por roles.

# V11 FINAL — Demo local-first estable

## Corrección principal
El flujo Cliente → Cocina → Administración ya no depende de que Render conserve la misma memoria o base temporal entre pantallas.

### Cómo funciona
- El pedido de la demostración se guarda en `localStorage` del navegador.
- Al pagar, el estado `Pagado / Recibido` queda disponible inmediatamente para Cocina.
- Cocina actualiza el mismo pedido en el navegador: Recibido → En preparación → Listo → Entregado.
- Administración lee el mismo pedido y muestra total, tiempos, estado y factura.
- La API del servidor se mantiene como respaldo, pero ya no es la fuente única de la demo.
- El PDF se genera de forma stateless enviando los datos del pedido al servidor, por lo que no depende de SQLite ni de memoria de Render.

## Resultado
Un solo enlace y un recorrido estable en el mismo dispositivo/navegador:
Cliente → Pago → Cocina → Administración → Factura PDF.

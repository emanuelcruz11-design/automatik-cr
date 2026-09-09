# V10 - Cocina corregida con almacenamiento compartido SQLite

## Problema resuelto
El cliente podía pagar correctamente, pero al entrar a Cocina aparecía 0 pedidos.

## Cambio principal
- Se eliminó el almacenamiento temporal en la lista Python `ORDERS`.
- Los pedidos de la demo ahora se guardan en una base SQLite compartida en `/tmp/automatik_restaurante_demo.db`.
- Cliente, Cocina y Administración leen la misma fuente de datos.
- La cocina solo muestra pedidos pagados.
- Se mantiene un worker en Gunicorn como medida adicional de estabilidad para la demo.

## Flujo
Cliente → pago → pedido persistido → Cocina → Administración → Factura PDF.

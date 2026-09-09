# V9.1 - Cocina visible después del pago

## Corrección aplicada
- Se ajustó el `startCommand` en `render.yaml` para ejecutar Gunicorn con **1 worker**.
- Esto evita que la demo guarde pedidos en memorias separadas entre workers.
- Ahora, cuando el cliente paga y entra a Cocina, el pedido sí aparece correctamente.

## Motivo técnico
La demo usa una lista en memoria (`ORDERS`) dentro de `app.py`.
Con varios workers de Gunicorn, cada worker tiene su propia memoria, por lo que Cliente y Cocina podían ver datos distintos.

## Nuevo comando
`gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4`

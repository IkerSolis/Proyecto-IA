from decimal import Decimal
from django.db import transaction
from catalog.models import Producto
from .models import Venta, VentaItem

def registrar_venta(empresa_id, items_data, cliente=None, vendedor=None):
    if not items_data:
        raise ValueError("La venta debe tener al menos un producto.")

    with transaction.atomic():
        venta = Venta.objects.create(
            empresa_id=empresa_id, 
            total_venta=0,
            nombre_cliente=cliente,
            nombre_vendedor=vendedor
        )
        total_venta = Decimal('0.00')

        for item in items_data:
            producto_id = item.get('producto_id')
            try:
                cantidad = int(item.get('cantidad', 0))
            except ValueError:
                raise ValueError("La cantidad debe ser un número entero.")

            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            try:
                # Bloqueo pesimista para evitar condiciones de carrera
                producto = Producto.objects.select_for_update().get(
                    id=producto_id,
                    empresa_id=empresa_id,
                    estado='activo'
                )
            except Producto.DoesNotExist:
                raise ValueError(f"Producto con ID {producto_id} no encontrado o inactivo.")

            if producto.stock_actual < cantidad:
                raise ValueError(f"Stock insuficiente para el producto: {producto.nombre}. Disponible: {producto.stock_actual}")

            # Descontar stock
            producto.stock_actual -= cantidad
            producto.save()

            # Insertar item
            precio_unitario = producto.precio
            VentaItem.objects.create(
                venta=venta,
                producto=producto,
                empresa_id=empresa_id,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )

            total_venta += (precio_unitario * cantidad)

        # Actualizar total de la venta
        venta.total_venta = total_venta
        venta.save()

        return venta

def obtener_ventas(empresa_id):
    return Venta.objects.filter(empresa_id=empresa_id).prefetch_related('items', 'items__producto')

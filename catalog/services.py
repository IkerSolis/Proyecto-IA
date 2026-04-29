from decimal import Decimal
from .models import Producto

def crear_producto(empresa_id, datos):
    producto = Producto(
        nombre=datos['nombre'],
        descripcion=datos.get('descripcion'),
        precio=Decimal(str(datos['precio'])),
        stock_actual=datos.get('stock_actual', 0),
        estado='activo',
        empresa_id=empresa_id
    )
    producto.save()
    return producto

def obtener_productos(empresa_id, solo_activos=True):
    query = Producto.objects.filter(empresa_id=empresa_id)
    if solo_activos:
        query = query.filter(estado='activo')
    return query

def actualizar_producto(empresa_id, producto_id, datos):
    try:
        producto = Producto.objects.get(id=producto_id, empresa_id=empresa_id)
    except Producto.DoesNotExist:
        raise ValueError("Producto no encontrado o no pertenece a esta empresa.")
        
    if 'nombre' in datos:
        producto.nombre = datos['nombre']
    if 'descripcion' in datos:
        producto.descripcion = datos['descripcion']
    if 'precio' in datos:
        producto.precio = Decimal(str(datos['precio']))
    if 'stock_actual' in datos:
        producto.stock_actual = datos['stock_actual']
        
    producto.save()
    return producto

def desactivar_producto(empresa_id, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id, empresa_id=empresa_id)
    except Producto.DoesNotExist:
        raise ValueError("Producto no encontrado o no pertenece a esta empresa.")
        
    producto.estado = 'inactivo'
    producto.save()
    return producto

def verificar_disponibilidad(empresa_id, producto_id, cantidad_requerida):
    try:
        producto = Producto.objects.get(id=producto_id, empresa_id=empresa_id, estado='activo')
    except Producto.DoesNotExist:
        raise ValueError("Producto no encontrado o inactivo.")
        
    return producto.stock_actual >= cantidad_requerida

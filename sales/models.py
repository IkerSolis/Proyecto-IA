import uuid
from django.db import models
from iam.models import Empresa
from catalog.models import Producto

class Venta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    nombre_cliente = models.CharField(max_length=255, null=True, blank=True)
    nombre_vendedor = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'venta'

    def __str__(self):
        return f"Venta {self.id} - Total: {self.total_venta}"

class VentaItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    class Meta:
        managed = False
        db_table = 'venta_items'

    def __str__(self):
        return f"Item: {self.producto.nombre} x {self.cantidad}"

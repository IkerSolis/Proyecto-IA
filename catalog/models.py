import uuid
from django.db import models
from iam.models import Empresa

class Producto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock_actual = models.IntegerField(default=0)
    estado = models.CharField(max_length=20, default='activo')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'producto'

    def __str__(self):
        return self.nombre

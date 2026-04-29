import uuid
from django.db import models

class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    giro = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    logo_url = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=150, unique=True)
    password_hash = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'empresa'

    def __str__(self):
        return self.nombre

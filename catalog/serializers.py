from rest_framework import serializers

class ProductoSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    precio = serializers.DecimalField(max_digits=12, decimal_places=2)
    stock_actual = serializers.IntegerField(default=0, required=False)
    estado = serializers.CharField(read_only=True)

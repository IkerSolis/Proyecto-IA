from rest_framework import serializers

class VentaItemCreateSerializer(serializers.Serializer):
    producto_id = serializers.UUIDField()
    cantidad = serializers.IntegerField(min_value=1)

class VentaCreateSerializer(serializers.Serializer):
    nombre_cliente = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    nombre_vendedor = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    items = VentaItemCreateSerializer(many=True, allow_empty=False)

class VentaItemSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    producto_id = serializers.UUIDField(source='producto.id')
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    cantidad = serializers.IntegerField(read_only=True)
    precio_unitario = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

class VentaSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    nombre_cliente = serializers.CharField(read_only=True)
    nombre_vendedor = serializers.CharField(read_only=True)
    total_venta = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    fecha = serializers.DateTimeField(read_only=True)
    items = VentaItemSerializer(many=True, read_only=True)

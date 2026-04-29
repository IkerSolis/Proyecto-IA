from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductoSerializer
from .services import crear_producto, obtener_productos, actualizar_producto, desactivar_producto, verificar_disponibilidad

class ProductoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        empresa_id = request.user.id
        if not empresa_id:
            return Response({"error": "Token no contiene empresa_id"}, status=status.HTTP_403_FORBIDDEN)
            
        solo_activos = request.query_params.get('solo_activos', 'true').lower() == 'true'
        productos = obtener_productos(empresa_id, solo_activos)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        empresa_id = request.user.id
        if not empresa_id:
            return Response({"error": "Token no contiene empresa_id"}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = crear_producto(empresa_id, serializer.validated_data)
            return Response(ProductoSerializer(producto).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, producto_id):
        empresa_id = request.user.id
        if not empresa_id:
            return Response({"error": "Token no contiene empresa_id"}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ProductoSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                producto = actualizar_producto(empresa_id, producto_id, serializer.validated_data)
                return Response(ProductoSerializer(producto).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, producto_id):
        empresa_id = request.user.id
        if not empresa_id:
            return Response({"error": "Token no contiene empresa_id"}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            producto = desactivar_producto(empresa_id, producto_id)
            return Response({"mensaje": "Producto desactivado correctamente.", "id": str(producto.id)}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductoDisponibilidadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, producto_id):
        empresa_id = request.user.id
        if not empresa_id:
            return Response({"error": "Token no contiene empresa_id"}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            cantidad = int(request.query_params.get('cantidad', 1))
        except ValueError:
            return Response({"error": "La cantidad debe ser un número entero válido."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            disponible = verificar_disponibilidad(empresa_id, producto_id, cantidad)
            return Response({"producto_id": str(producto_id), "cantidad_requerida": cantidad, "disponible": disponible}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

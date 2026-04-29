from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import VentaCreateSerializer, VentaSerializer
from .services import registrar_venta, obtener_ventas

class VentaListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        empresa_id = request.user.id
        if not empresa_id:
            return Response({"error": "No autenticado."}, status=status.HTTP_403_FORBIDDEN)
            
        ventas = obtener_ventas(empresa_id)
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        empresa_id = request.user.id
        if not empresa_id:
            return Response({"error": "No autenticado."}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = VentaCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                venta = registrar_venta(
                    empresa_id, 
                    serializer.validated_data['items'],
                    cliente=serializer.validated_data.get('nombre_cliente'),
                    vendedor=serializer.validated_data.get('nombre_vendedor')
                )
                return Response(VentaSerializer(venta).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "Ocurrió un error inesperado al procesar la venta."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

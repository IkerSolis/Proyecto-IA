from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import OnboardingSerializer, LoginSerializer
from .services import crear_empresa, autenticar_empresa

class OnboardingView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OnboardingSerializer(data=request.data)
        if serializer.is_valid():
            try:
                empresa = crear_empresa(serializer.validated_data)
                return Response({
                    "mensaje": "Empresa registrada exitosamente.",
                    "id": str(empresa.id),
                    "email": empresa.email
                }, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tokens = autenticar_empresa(
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )
                return Response(tokens, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from .models import Empresa

class EmpresaJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
            return Empresa.objects.get(id=user_id)
        except Empresa.DoesNotExist:
            raise AuthenticationFailed("Empresa no encontrada", code="user_not_found")

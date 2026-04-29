from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Empresa

def crear_empresa(datos):
    """
    Crea una nueva empresa validando que el email no exista y encriptando el password.
    """
    if Empresa.objects.filter(email=datos['email']).exists():
        raise ValueError("El email ya está registrado.")
    
    empresa = Empresa(
        nombre=datos['nombre'],
        giro=datos.get('giro'),
        descripcion=datos.get('descripcion'),
        email=datos['email'],
        password_hash=make_password(datos['password'])
    )
    empresa.save()
    return empresa

def autenticar_empresa(email, password):
    """
    Verifica las credenciales y devuelve un par de tokens (refresh, access).
    """
    try:
        empresa = Empresa.objects.get(email=email)
    except Empresa.DoesNotExist:
        raise ValueError("Credenciales inválidas.")

    if not check_password(password, empresa.password_hash):
        raise ValueError("Credenciales inválidas.")

    refresh = RefreshToken()
    refresh['user_id'] = str(empresa.id)
    refresh['empresa_id'] = str(empresa.id)
    refresh['email'] = empresa.email

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

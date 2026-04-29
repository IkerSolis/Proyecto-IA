from django.db import connection

class TenantIsolationMiddleware:
    """
    Middleware que intercepta la petición HTTP, lee el JWT (si existe),
    extrae el empresa_id y configura la variable de sesión de PostgreSQL
    para asegurar el RLS (Row Level Security).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_id = None
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                from rest_framework_simplejwt.tokens import AccessToken
                access_token = AccessToken(token)
                tenant_id = access_token.get('empresa_id')
            except Exception:
                pass
        
        try:
            with connection.cursor() as cursor:
                if tenant_id:
                    cursor.execute("SET app.current_tenant_id = %s", [str(tenant_id)])
                else:
                    # UUID nulo para peticiones no autenticadas, evita fugas de conexión
                    cursor.execute("SET app.current_tenant_id = '00000000-0000-0000-0000-000000000000'")
        except Exception as e:
            # Si no hay DB configurada correctamente o falla la conexión, permitimos que siga (puede que la vista no requiera DB)
            pass

        response = self.get_response(request)
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("RESET app.current_tenant_id")
        except Exception:
            pass
            
        return response

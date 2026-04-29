import os
import django
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexos_erp.settings')
django.setup()

def check_database_connection():
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
        print(f"¡Conexión exitosa a la base de datos PostgreSQL '{db_conn.settings_dict['NAME']}'!")
        
        # Validar si las tablas del query existen
        c.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = [row[0] for row in c.fetchall()]
        required_tables = ['empresa', 'producto', 'venta', 'venta_items']
        
        missing = [t for t in required_tables if t not in tables]
        
        if not missing:
            print("Se ha verificado la integridad: Todas las tablas principales existen.")
        else:
            print(f"Advertencia: Faltan las siguientes tablas en la base de datos: {', '.join(missing)}")
            
    except Exception as e:
        print("Error de conexión a la base de datos.")
        print("Esto generalmente significa que las credenciales son incorrectas o el servicio no está corriendo.")
        print(f"Detalles técnicos: {e}")
        print("Por favor verifica las variables DB_PASSWORD, DB_USER y demás en tu archivo .env")

if __name__ == '__main__':
    check_database_connection()

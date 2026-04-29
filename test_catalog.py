import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexos_erp.settings')
django.setup()

from rest_framework.test import APIClient
from iam.models import Empresa
from catalog.models import Producto

# Cleanup previous tests if any
Empresa.objects.filter(email='test_cat@empresa.com').delete()

from iam.services import crear_empresa
empresa = crear_empresa({
    'nombre': 'Cat Empresa',
    'email': 'test_cat@empresa.com',
    'password': 'password123'
})

client = APIClient()
response = client.post('/api/iam/login/', {'email': 'test_cat@empresa.com', 'password': 'password123'}, format='json')
token = response.json()['access']
client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

print("--- Testing Create Producto ---")
response = client.post('/api/catalog/productos/', {
    'nombre': 'Tomate Saladette',
    'descripcion': 'Caja 10kg',
    'precio': '150.50',
    'stock_actual': 100
}, format='json')
print("Status:", response.status_code)
prod_data = response.json()
print("Response:", prod_data)
prod_id = prod_data.get('id')

if prod_id:
    print("\n--- Testing List Productos ---")
    response = client.get('/api/catalog/productos/')
    print("Status:", response.status_code)
    print("Count:", len(response.json()))

    print("\n--- Testing Disponibilidad ---")
    response = client.get(f'/api/catalog/productos/{prod_id}/disponibilidad/?cantidad=50')
    print("Status:", response.status_code)
    print("Response:", response.json())

    print("\n--- Testing Soft Delete ---")
    response = client.delete(f'/api/catalog/productos/{prod_id}/')
    print("Status:", response.status_code)
    print("Response:", response.json())
    
    print("\n--- List after Delete (solo_activos=true) ---")
    response = client.get('/api/catalog/productos/')
    print("Count:", len(response.json()))

# Cleanup
Producto.objects.filter(empresa=empresa).delete()
Empresa.objects.filter(id=empresa.id).delete()

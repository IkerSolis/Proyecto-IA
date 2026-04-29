import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexos_erp.settings')
django.setup()

from rest_framework.test import APIClient
from iam.models import Empresa
from catalog.models import Producto
from sales.models import Venta

# Cleanup previous tests if any
Empresa.objects.filter(email='test_sales@empresa.com').delete()

from iam.services import crear_empresa
empresa = crear_empresa({
    'nombre': 'Sales Empresa',
    'email': 'test_sales@empresa.com',
    'password': 'password123'
})

client = APIClient()
response = client.post('/api/iam/login/', {'email': 'test_sales@empresa.com', 'password': 'password123'}, format='json')
token = response.json()['access']
client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

# Create some products to sell
print("--- Creating Catalog Products ---")
prod1_res = client.post('/api/catalog/productos/', {
    'nombre': 'Laptop',
    'precio': '1500.00',
    'stock_actual': 10
}, format='json')
prod1_id = prod1_res.json()['id']

prod2_res = client.post('/api/catalog/productos/', {
    'nombre': 'Mouse',
    'precio': '25.50',
    'stock_actual': 50
}, format='json')
prod2_id = prod2_res.json()['id']

print("Productos creados:", prod1_id, prod2_id)

print("\n--- Testing Venta Creation ---")
venta_res = client.post('/api/sales/ventas/', {
    'items': [
        {'producto_id': prod1_id, 'cantidad': 2},
        {'producto_id': prod2_id, 'cantidad': 5}
    ]
}, format='json')

print("Status:", venta_res.status_code)
import json
print("Response:", json.dumps(venta_res.json(), indent=2))

print("\n--- Testing Failed Venta (Stock Insuficiente) ---")
failed_res = client.post('/api/sales/ventas/', {
    'items': [
        {'producto_id': prod1_id, 'cantidad': 20}
    ]
}, format='json')
print("Status:", failed_res.status_code)
print("Response:", failed_res.json())

print("\n--- Verify Stock Discount ---")
check_prod1 = client.get('/api/catalog/productos/')
for p in check_prod1.json():
    print(f"{p['nombre']} - Stock: {p['stock_actual']}")

# Cleanup
Venta.objects.filter(empresa=empresa).delete()
Producto.objects.filter(empresa=empresa).delete()
Empresa.objects.filter(id=empresa.id).delete()

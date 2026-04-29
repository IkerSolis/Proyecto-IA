import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexos_erp.settings')
django.setup()

from rest_framework.test import APIClient
from iam.models import Empresa

# Cleanup if already exists
Empresa.objects.filter(email='test@empresa.com').delete()

client = APIClient()

print("--- Testing Onboarding ---")
response = client.post('/api/iam/onboarding/', {
    'nombre': 'Empresa Test',
    'giro': 'Tecnología',
    'email': 'test@empresa.com',
    'password': 'password123'
}, format='json')
print("Status:", response.status_code)
print("Response:", response.json())

print("\n--- Testing Login ---")
response = client.post('/api/iam/login/', {
    'email': 'test@empresa.com',
    'password': 'password123'
}, format='json')
print("Status:", response.status_code)
if response.status_code == 200:
    print("Tokens obtenidos correctamente (refresh y access)")
else:
    print("Response:", response.json())

# Cleanup
Empresa.objects.filter(email='test@empresa.com').delete()

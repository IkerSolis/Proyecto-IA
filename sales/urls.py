from django.urls import path
from .views import VentaListView

urlpatterns = [
    path('ventas/', VentaListView.as_view(), name='venta_list'),
]

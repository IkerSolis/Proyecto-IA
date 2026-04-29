from django.urls import path
from .views import ProductoListView, ProductoDetailView, ProductoDisponibilidadView

urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='producto_list'),
    path('productos/<uuid:producto_id>/', ProductoDetailView.as_view(), name='producto_detail'),
    path('productos/<uuid:producto_id>/disponibilidad/', ProductoDisponibilidadView.as_view(), name='producto_disponibilidad'),
]

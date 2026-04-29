from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('onboarding/', views.onboarding_view, name='onboarding'),
    path('inventario/', views.inventario_view, name='inventario'),
    path('pos/', views.pos_view, name='pos'),
    path('settings/', views.settings_view, name='settings'),
]

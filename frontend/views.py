from django.shortcuts import render

def login_view(request):
    return render(request, 'login.html')

def onboarding_view(request):
    return render(request, 'onboarding.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def inventario_view(request):
    return render(request, 'inventario.html')

def pos_view(request):
    return render(request, 'pos.html')

def settings_view(request):
    return render(request, 'settings.html')

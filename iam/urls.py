from django.urls import path
from .views import OnboardingView, LoginView

urlpatterns = [
    path('onboarding/', OnboardingView.as_view(), name='onboarding'),
    path('login/', LoginView.as_view(), name='login'),
]

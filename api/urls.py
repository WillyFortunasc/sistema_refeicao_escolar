from django.urls import path
from .views import RegistroView, LoginView, health_check

urlpatterns = [
    path('health/', health_check),
    path('login/', LoginView.as_view()),
    path('registro/', RegistroView.as_view()),
]


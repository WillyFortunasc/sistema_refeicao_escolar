from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegistroView,
    LoginView,
    health_check,
    EstudanteViewSet
)

router = DefaultRouter()
router.register(r'estudantes', EstudanteViewSet)

urlpatterns = [
    path('health/', health_check),
    path('login/', LoginView.as_view()),
    path('registro/', RegistroView.as_view()),
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegistroView,
    LoginView,
    health_check,
    EstudanteViewSet,
    DigitalViewSet,
    RefeicaoViewSet
)

router = DefaultRouter()
router.register(r'estudantes', EstudanteViewSet)
router.register(r'digitais', DigitalViewSet)
router.register(r'refeicoes', RefeicaoViewSet)

urlpatterns = [
    path('health/', health_check),
    path('login/', LoginView.as_view()),
    path('registro/', RegistroView.as_view()),
    path('', include(router.urls)),
]

from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
]
## coloquei agora 01 de abril
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]

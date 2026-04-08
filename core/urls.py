from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "API rodando 🚀",
        "endpoints": [
            "/api/health/",
            "/api/login/",
            "/admin/"
        ]
    })

urlpatterns = [
    path('', home),  # ✅ agora a raiz funciona
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

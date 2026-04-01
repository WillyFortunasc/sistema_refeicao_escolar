from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]


from django.urls import path
from .views import RegistroView, LoginView

urlpatterns = [
    path("registro/", RegistroView.as_view(), name="registro"),
    path("login/", LoginView.as_view(), name="login"),
]

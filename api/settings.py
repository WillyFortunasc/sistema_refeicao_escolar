urlpatterns += [
    path("auth/", include("social_django.urls", namespace="social")),
]

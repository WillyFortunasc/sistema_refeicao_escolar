INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",   # se estiver usando DRF
    "core",             # <-- adicione aqui
]
AUTH_USER_MODEL = "core.Usuario"

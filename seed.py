"""
Popula o banco com usuários de cada papel para testes.
Execute: python seed.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from api.models import Usuario

USUARIOS = [
    {"email": "admin@sistema.com",    "nome": "Admin",    "papel": "admin",    "senha": "Admin@123"},
    {"email": "operador@sistema.com", "nome": "Operador", "papel": "operador", "senha": "Oper@123"},
    {"email": "fiscal@sistema.com",   "nome": "Fiscal",   "papel": "fiscal",   "senha": None},
    {"email": "gestor@sistema.com",   "nome": "Gestor",   "papel": "gestor",   "senha": "Gest@123"},
    {"email": "empresa@sistema.com",  "nome": "Empresa",  "papel": "empresa",  "senha": "Empr@123"},
]

for u in USUARIOS:
    if not Usuario.objects.filter(email=u["email"]).exists():
        Usuario.objects.create_user(
            email=u["email"],
            nome=u["nome"],
            papel=u["papel"],
            senha=u["senha"],
        )
        print(f"  criado → {u['email']}  [{u['papel']}]")
    else:
        print(f"  já existe → {u['email']}")

print("\nSeed concluído.")

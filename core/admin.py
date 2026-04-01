from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Campos que vão aparecer na listagem de usuários no admin
    list_display = ("email", "nome", "papel", "ativo", "ultimo_acesso", "is_staff")
    list_filter = ("papel", "ativo", "is_staff", "is_superuser")
    search_fields = ("email", "nome")

    # Campos que aparecem no formulário de edição
    fieldsets = (
        (None, {"fields": ("email", "senha")}),
        ("Informações pessoais", {"fields": ("nome", "papel", "ativo", "ultimo_acesso")}),
        ("Permissões", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    # Campos usados ao criar novo usuário
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nome", "papel", "senha1", "senha2"),
        }),
    )

    ordering = ("email",)

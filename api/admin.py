from django.contrib import admin
from .models import Usuario, Estudante


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("email", "nome", "papel", "ativo")
    search_fields = ("email", "nome")
    list_filter = ("papel", "ativo")


@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "matricula", "curso", "turma", "ativo")
    search_fields = ("nome_completo", "matricula")
    list_filter = ("curso", "turma", "ativo")
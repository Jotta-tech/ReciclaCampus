from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = (
        "matricula", "first_name", "last_name",
        "curso", "email", "is_staff", "is_active"
    )
    list_filter = ("is_staff", "is_active", "curso")
    search_fields = ("matricula", "first_name", "last_name", "email")
    ordering = ("matricula",)

    # Adiciona matricula e curso na tela de edição do admin
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Dados acadêmicos", {
            "fields": ("matricula", "curso")
        }),
    )

    # Adiciona matricula e curso na tela de criação do admin
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Dados acadêmicos", {
            "fields": ("matricula", "curso")
        }),
    )
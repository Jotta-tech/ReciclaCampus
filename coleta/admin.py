from django.contrib import admin

from .models import PontoColeta, RegistroReciclagem, Residuo


@admin.register(Residuo)
class ResiduoAdmin(admin.ModelAdmin):
    list_display = ("icone", "nome", "pontos", "ativo", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("nome",)
    list_editable = ("pontos", "ativo")
    ordering = ("nome",)


@admin.register(PontoColeta)
class PontoColetaAdmin(admin.ModelAdmin):
    list_display = ("nome", "localizacao", "codigo", "ativo", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("nome", "localizacao", "codigo")
    readonly_fields = ("codigo", "criado_em")
    ordering = ("nome",)
    fieldsets = (
        (None, {
            "fields": ("nome", "localizacao", "descricao")
        }),
        ("QR Code", {
            "fields": ("codigo",),
            "description": "Este código é usado no QR Code do ponto. Não edite manualmente."
        }),
        ("Controle", {
            "fields": ("ativo", "criado_em")
        }),
    )


@admin.register(RegistroReciclagem)
class RegistroReciclagemAdmin(admin.ModelAdmin):
    list_display = (
        "usuario", "residuo", "quantidade", "pontos",
        "ponto_coleta", "confirmado", "data"
    )
    list_filter = ("confirmado", "residuo", "ponto_coleta", "data")
    search_fields = (
        "usuario__matricula",
        "usuario__first_name",
        "usuario__username",
        "residuo__nome",
    )
    readonly_fields = ("pontos", "data")
    date_hierarchy = "data"
    ordering = ("-data",)
    list_editable = ("confirmado",)
    autocomplete_fields = ("usuario", "residuo", "ponto_coleta")
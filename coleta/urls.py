from django.urls import path

from . import qrcode_utils, views

app_name = "coleta"

urlpatterns = [
    path(
        "ponto/<uuid:codigo>/",
        views.ponto_detalhe,
        name="ponto_detalhe"
    ),
    path(
        "ponto/<uuid:codigo>/registrar/",
        views.registrar_coleta_view,
        name="registrar"
    ),
    path(
        "qr/<uuid:codigo>.png",
        qrcode_utils.qr_code_view,
        name="qr_code"
    ),
    path("ranking/", views.ranking_view, name="ranking"),
        path("historico/", views.historico_view, name="historico"),
            path("escanear/", views.escanear_view, name="escanear"),
                path("mapa/", views.mapa_view, name="mapa"),
]
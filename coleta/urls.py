from django.urls import path

from . import views
from . import qrcode_utils


app_name = "coleta"

urlpatterns = [
    path("ponto/<uuid:codigo>/", views.ponto_detalhe, name="ponto_detalhe"),
    path("ponto/<uuid:codigo>/registrar/", views.registrar_coleta_view, name="registrar"),
    path("qr/<uuid:codigo>.png", qrcode_utils.qr_code_view, name="qr_code"),
]
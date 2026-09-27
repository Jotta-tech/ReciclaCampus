import io
import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import PontoColeta


def qr_code_view(request, codigo):
    """
    Gera dinamicamente um QR Code (PNG) apontando pra URL de registro
    do ponto de coleta identificado por `codigo`.
    """
    ponto = get_object_or_404(PontoColeta, codigo=codigo)

    # URL que o QR vai apontar
    url_registro = request.build_absolute_uri(f"/coleta/ponto/{ponto.codigo}/")

    # Gera o QR Code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=2,
    )
    qr.add_data(url_registro)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#166534", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")
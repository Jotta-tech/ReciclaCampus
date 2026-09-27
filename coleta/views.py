from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import PontoColeta, Residuo
from . import services


@login_required
def ponto_detalhe(request, codigo):
    """
    Tela que aparece DEPOIS que o usuário escaneia o QR Code.
    Mostra o ponto + lista de resíduos disponíveis pra selecionar.
    """
    ponto = get_object_or_404(PontoColeta, codigo=codigo, ativo=True)
    residuos = Residuo.objects.filter(ativo=True).order_by("nome")

    return render(
        request,
        "coleta/ponto_detalhe.html",
        {
            "ponto": ponto,
            "residuos": residuos,
        },
    )


@login_required
def registrar_coleta_view(request, codigo):
    """
    Recebe o POST da tela de detalhe.
    Registra a coleta e volta pro dashboard.
    """
    ponto = get_object_or_404(PontoColeta, codigo=codigo, ativo=True)

    if request.method != "POST":
        return redirect("coleta:ponto_detalhe", codigo=codigo)

    residuo_id = request.POST.get("residuo")
    quantidade = request.POST.get("quantidade", 1)

    # Validações básicas
    try:
        quantidade = max(1, int(quantidade))
    except (TypeError, ValueError):
        quantidade = 1

    residuo = get_object_or_404(Residuo, id=residuo_id, ativo=True)

    # Registra
    registro = services.registrar_coleta(
        usuario=request.user,
        ponto=ponto,
        residuo=residuo,
        quantidade=quantidade,
    )

    # Mensagem de sucesso (aparece no dashboard)
    messages.success(
        request,
        f"Você reciclou {quantidade}x {residuo.nome} e ganhou "
        f"{registro.pontos} pontos! 🎉"
    )

    return redirect("dashboard")
import json
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

    # Validações básicas de quantidade
    try:
        quantidade = max(1, int(quantidade))
    except (TypeError, ValueError):
        quantidade = 1

    # Busca o resíduo de forma segura (sem derrubar a página com 404)
    try:
        residuo = Residuo.objects.get(id=residuo_id, ativo=True)
    except (Residuo.DoesNotExist, ValueError):
        messages.error(
            request, 
            "Material inválido ou indisponível. Por favor, selecione outro."
        )
        return redirect("coleta:ponto_detalhe", codigo=codigo)

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
@login_required
def ranking_view(request):
    """
    Página de ranking geral: lista os estudantes ordenados por pontos.
    Destaca os 3 primeiros e mostra a posição do usuário logado.
    """
    lista = services.ranking()  # já ordenado por pontos (desc)
    posicao = services.posicao_usuario(request.user)

    # Separa o pódio (top 3) do resto
    podio = lista[:3]
    resto = lista[3:]

    return render(
        request,
        "coleta/ranking.html",
        {
            "podio": podio,
            "resto": resto,
            "posicao": posicao,
        },
    )

@login_required
def historico_view(request):
    """
    Página de histórico completo de reciclagem do usuário logado.
    """
    registros = services.historico_usuario(request.user)

    return render(
        request,
        "coleta/historico.html",
        {
            "registros": registros,
            "total_pontos": services.total_pontos(request.user),
            "total_itens": services.total_itens(request.user),
            "total_registros": services.total_registros(request.user),
        },
    )

@login_required
def escanear_view(request):
    """
    Página que abre a câmera para ler o QR Code de um ponto de coleta.
    A leitura e o redirecionamento são feitos via JavaScript no template.
    """
    return render(request, "coleta/escanear.html")

@login_required
def mapa_view(request):
    """
    Página com mapa dos pontos de coleta ativos.
    Os pontos são passados como JSON para o template (Leaflet consome).
    """
    pontos = PontoColeta.objects.filter(ativo=True).order_by("nome")

    pontos_json = [
        {
            "nome": p.nome,
            "localizacao": p.localizacao,
            "descricao": p.descricao,
            "codigo": str(p.codigo),
            "latitude": p.latitude,
            "longitude": p.longitude,
        }
        for p in pontos
    ]

    return render(
        request,
        "coleta/mapa.html",
        {"pontos_json": pontos_json},
    )
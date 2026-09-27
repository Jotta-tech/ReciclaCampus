from datetime import date

from django.db.models import Sum, Q, Count
from django.utils import timezone

from .models import RegistroReciclagem


# ============================================================
# Registro de coleta
# ============================================================

def registrar_coleta(usuario, ponto, residuo, quantidade=1):
    """
    Cria um RegistroReciclagem e retorna o objeto criado.
    Os pontos são calculados automaticamente pelo save() do model.
    """
    if quantidade < 1:
        quantidade = 1

    registro = RegistroReciclagem.objects.create(
        usuario=usuario,
        ponto_coleta=ponto,
        residuo=residuo,
        quantidade=quantidade,
    )
    return registro


# ============================================================
# Estatísticas do usuário
# ============================================================

def total_pontos(usuario):
    """Soma dos pontos de todos os registros confirmados do usuário."""
    resultado = RegistroReciclagem.objects.filter(
        usuario=usuario,
        confirmado=True,
    ).aggregate(total=Sum("pontos"))
    return resultado["total"] or 0


def total_itens(usuario):
    """Soma da quantidade de itens reciclados (unidades)."""
    resultado = RegistroReciclagem.objects.filter(
        usuario=usuario,
        confirmado=True,
    ).aggregate(total=Sum("quantidade"))
    return resultado["total"] or 0


def total_registros(usuario):
    """Quantidade de registros de coleta feitos pelo usuário."""
    return RegistroReciclagem.objects.filter(
        usuario=usuario,
        confirmado=True,
    ).count()


# ============================================================
# Níveis
# ============================================================

# Lista de níveis. Edite aqui se quiser ajustar os limites/nomes.
NIVEIS = [
    {"nivel": 1, "nome": "Iniciante Verde", "min_pontos": 0,    "max_pontos": 500},
    {"nivel": 2, "nome": "Guardião Verde",  "min_pontos": 500,  "max_pontos": 2000},
    {"nivel": 3, "nome": "Herói Sustentável","min_pontos": 2000, "max_pontos": 5000},
    {"nivel": 4, "nome": "Lenda do Campus", "min_pontos": 5000, "max_pontos": None},
]


def nivel_usuario(usuario):
    """
    Retorna um dicionário com o nível atual do usuário:
    {
        "nivel": 2,
        "nome": "Guardião Verde",
        "min_pontos": 500,
        "max_pontos": 2000,
        "progresso": 45.0,   # % dentro do nível atual
        "faltam": 750,       # pontos que faltam pro próximo nível
        "proximo_nome": "Herói Sustentável",
    }
    """
    pontos = total_pontos(usuario)

    nivel_atual = NIVEIS[0]
    for nivel in NIVEIS:
        if pontos >= nivel["min_pontos"]:
            nivel_atual = nivel
        else:
            break

    proximo = None
    for nivel in NIVEIS:
        if nivel["nivel"] == nivel_atual["nivel"] + 1:
            proximo = nivel
            break

    if nivel_atual["max_pontos"] is None:
        # Usuário já está no topo
        progresso = 100.0
        faltam = 0
        proximo_nome = None
    else:
        faixa = nivel_atual["max_pontos"] - nivel_atual["min_pontos"]
        dentro = pontos - nivel_atual["min_pontos"]
        progresso = round((dentro / faixa) * 100, 1) if faixa else 0.0
        faltam = max(0, nivel_atual["max_pontos"] - pontos)
        proximo_nome = proximo["nome"] if proximo else None

    return {
        "nivel": nivel_atual["nivel"],
        "nome": nivel_atual["nome"],
        "min_pontos": nivel_atual["min_pontos"],
        "max_pontos": nivel_atual["max_pontos"],
        "progresso": progresso,
        "faltam": faltam,
        "proximo_nome": proximo_nome,
    }


# ============================================================
# Ranking
# ============================================================

def ranking(limite=None, apenas_mes_atual=False, curso=None):
    """
    Retorna lista de usuários ordenada por pontos, no formato:
    [{"usuario": <Usuario>, "pontos": 1250}, ...]

    Parâmetros:
    - limite: quantos retornar (None = todos)
    - apenas_mes_atual: se True, considera só registros do mês atual
    - curso: se passado, filtra por curso
    """
    from usuarios.models import Usuario

    filtros = {"confirmado": True}

    if apenas_mes_atual:
        hoje = timezone.localdate()
        filtros["data__year"] = hoje.year
        filtros["data__month"] = hoje.month

    qs = (
        Usuario.objects
        .filter(registros_reciclagem__confirmado=True)
        .annotate(pontos_total=Sum("registros_reciclagem__pontos"))
        .order_by("-pontos_total")
    )

    if apenas_mes_atual:
        # Anotação condicional para o mês
        qs = (
            Usuario.objects
            .annotate(
                pontos_total=Sum(
                    "registros_reciclagem__pontos",
                    filter=Q(
                        registros_reciclagem__confirmado=True,
                        registros_reciclagem__data__year=hoje.year,
                        registros_reciclagem__data__month=hoje.month,
                    ),
                )
            )
            .filter(pontos_total__gt=0)
            .order_by("-pontos_total")
        )

    if curso:
        qs = qs.filter(curso=curso)

    if limite:
        qs = qs[:limite]

    return [{"usuario": u, "pontos": u.pontos_total or 0} for u in qs]


def posicao_usuario(usuario):
    """
    Retorna a posição do usuário no ranking geral (1 = primeiro).
    Retorna None se o usuário não tiver nenhum registro confirmado.
    """
    from usuarios.models import Usuario

    pontos_usuario = total_pontos(usuario)
    if pontos_usuario == 0:
        return None

    qs = (
        Usuario.objects
        .annotate(pontos_total=Sum(
            "registros_reciclagem__pontos",
            filter=Q(registros_reciclagem__confirmado=True),
        ))
        .filter(pontos_total__gt=pontos_usuario)
        .count()
    )
    return qs + 1


# ============================================================
# Últimas coletas (pro Dashboard)
# ============================================================

def ultimas_coletas(usuario, limite=3):
    """Retorna as últimas N coletas confirmadas do usuário."""
    return (
        RegistroReciclagem.objects
        .filter(usuario=usuario, confirmado=True)
        .select_related("residuo", "ponto_coleta")
        .order_by("-data")[:limite]
    )
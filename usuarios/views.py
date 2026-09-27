from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from coleta import services


def home(request):
    return render(request, 'usuarios/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')

        user = authenticate(
            request,
            username=matricula,
            password=senha
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(
            request,
            'usuarios/login.html',
            {'erro': 'Matrícula ou senha incorretas.'}
        )

    return render(request, 'usuarios/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    usuario = request.user

    contexto = {
        "total_pontos": services.total_pontos(usuario),
        "total_itens": services.total_itens(usuario),
        "total_registros": services.total_registros(usuario),
        "nivel": services.nivel_usuario(usuario),
        "posicao": services.posicao_usuario(usuario),
        "ultimas_coletas": services.ultimas_coletas(usuario, limite=3),
    }

    return render(request, 'usuarios/dashboard.html', contexto)
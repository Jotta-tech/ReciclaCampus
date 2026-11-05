from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from coleta import services

from .forms import CadastroUsuarioForm


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
            
            # Verifica se o Django guardou uma URL de destino (ex.: o QR Code)
            next_url = request.POST.get('next') or request.GET.get('next')
            
            if next_url:
                return redirect(next_url)
                
            return redirect('dashboard')

        return render(
            request,
            'usuarios/login.html',
            {'erro': 'Matrícula ou senha incorretas.'}
        )

    return render(request, 'usuarios/login.html')


def cadastro_view(request):
    """
    Tela de cadastro de estudante.

    GET  -> mostra o formulário vazio.
    POST -> valida; se ok, salva o usuário, loga automaticamente
            e redireciona pro dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            login(request, usuario, backend='usuarios.backends.MatriculaBackend')
            messages.success(
                request,
                f"Bem-vindo(a), {usuario.first_name}! Sua conta foi criada com sucesso. 🎉"
            )
            return redirect('dashboard')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


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
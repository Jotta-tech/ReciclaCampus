from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'usuarios/home.html')


def login_view(request):
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

def dashboard(request):
    return render(request, 'usuarios/dashboard.html')
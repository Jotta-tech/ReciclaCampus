from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class CadastroUsuarioForm(UserCreationForm):
    """
    Formulário de cadastro de estudante.
    """

    class Meta:
        model = Usuario
        fields = (
            "matricula",
            "first_name",
            "last_name",
            "email",
            "curso",
        )
        labels = {
            "matricula": "Matrícula",
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
            "curso": "Curso",
        }
        widgets = {
            "matricula": forms.TextInput(attrs={"placeholder": "Digite sua matrícula"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Digite seu nome"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Digite seu sobrenome"}),
            "email": forms.EmailInput(attrs={"placeholder": "Digite seu e-mail"}),
            "curso": forms.TextInput(attrs={"placeholder": "Ex.: Engenharia de Software"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Senha"
        self.fields["password1"].widget.attrs["placeholder"] = "Crie uma senha"
        self.fields["password2"].label = "Confirme a senha"
        self.fields["password2"].widget.attrs["placeholder"] = "Repita a senha"

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = usuario.matricula
        if commit:
            usuario.save()
        return usuario
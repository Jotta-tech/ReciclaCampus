from django.contrib.auth.backends import BaseBackend
from .models import Usuario


class MatriculaBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            usuario = Usuario.objects.get(matricula=username)

            if usuario.check_password(password):
                return usuario

        except Usuario.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from coleta.models import Residuo, PontoColeta, RegistroReciclagem
import uuid

Usuario = get_user_model()

class ReciclaCampusTests(TestCase):

    def setUp(self):
        # Esse método roda ANTES de cada teste. 
        # Aqui criamos um "banco de dados de mentira" só para os testes.
        
        # 1. Cria um usuário de teste
        self.user = Usuario.objects.create_user(
            username="12345", 
            matricula="12345", 
            password="senha_segura", 
            first_name="Aluno Teste",
            curso="Engenharia"
        )
        
        # 2. Cria um resíduo que vale 10 pontos
        self.residuo = Residuo.objects.create(
            nome="Plástico Teste",
            pontos=10,
            ativo=True
        )
        
        # 3. Cria um ponto de coleta
        self.ponto = PontoColeta.objects.create(
            nome="Lixeira Teste",
            localizacao="Bloco A",
            codigo=uuid.uuid4()
        )

    def test_aluno_deslogado_nao_pode_descartar(self):
        """Testa se quem não está logado é barrado ao tentar descartar."""
        url = reverse('coleta:registrar', args=[self.ponto.codigo])
        resposta = self.client.post(url, {'residuo': self.residuo.id, 'quantidade': 2})
        
        # Espera que o Django redirecione para o login (status 302)
        self.assertEqual(resposta.status_code, 302)
        # E que NENHUM registro tenha sido criado no banco
        self.assertEqual(RegistroReciclagem.objects.count(), 0)

    def test_calculo_de_pontos_automatico(self):
        """Testa se 3 itens de 10 pontos resultam em 30 pontos e viram registro."""
        # Faz o login "fake" do aluno
        self.client.login(matricula="12345", password="senha_segura")
        
        url = reverse('coleta:registrar', args=[self.ponto.codigo])
        
        # Envia o formulário de descarte
        self.client.post(url, {'residuo': self.residuo.id, 'quantidade': 3})
        
        # Verifica se o registro foi criado
        self.assertEqual(RegistroReciclagem.objects.count(), 1)
        
        # Verifica se o cálculo de 3 * 10 = 30 está certo
        registro = RegistroReciclagem.objects.first()
        self.assertEqual(registro.pontos, 30)

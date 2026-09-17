###### FASE 1 ############ PLANEJAMENTO ###########
# INTRODUÇÃO
O ReciclaCampus é um sistema desenvolvido com o objetivo de incentivar a prática da reciclagem no ambiente universitário por meio de um sistema de pontuação e gamificação.



# PROBLEMA
Apesar da existência de lixeiras destinadas à coleta seletiva, muitos estudantes não possuem incentivo suficiente para realizar o descarte correto dos resíduos. Dessa forma, o ReciclaCampus busca utilizar tecnologia e gamificação para estimular a participação dos alunos.



# OBJETIVO
Desenvolver um sistema que incentive a comunidade acadêmica a realizar o descarte correto de materiais recicláveis através de pontuação, ranking e localização das lixeiras.


# REQUISITOS FUNCIONAIS
RF01	O sistema deve permitir o cadastro de usuários
RF02	O sistema deve permitir login
RF03	O sistema deve identificar a lixeira através de QR Code
RF04	O sistema deve permitir registrar um descarte
RF05	O sistema deve atribuir pontos ao usuário
RF06	O sistema deve apresentar o ranking
RF07	O sistema deve apresentar a localização das lixeiras
RF08	O sistema deve permitir campanhas de pontos em dobro

# REQUISITOS NÃO FUNCIONAIS
RNF01	O sistema deve possuir autenticação segura
RNF02	A interface deve ser responsiva
RNF03	A API deve possuir comunicação segura
RNF04	O sistema deve apresentar boa disponibilidade
RNF05	O código deve ser organizado e documentado

# REGRAS DE NEGÓCIO 
Cada tipo de material possui uma quantidade específica de pontos.

Plástico → 10 pontos
Papel    → 8 pontos
Metal    → 15 pontos
Vidro    → 12 pontos
Orgânico → X pontos

Durante uma campanha de pontos em dobro, a pontuação recebida pelo usuário será multiplicada por 2.

Exemplo:

Plástico = 10 pontos

Campanha ativa:
10 × 2 = 20 pontos


# OBJETIVO ESPECÍFICOS
Incentivar a reciclagem dentro da universidade;
Registrar os descartes realizados pelos usuários;
Atribuir pontos de acordo com o material descartado;
Criar um ranking entre os participantes;
Disponibilizar a localização das lixeiras;
Permitir campanhas de pontuação em dobro;
Utilizar QR Codes para identificar as lixeiras.


###### FASE 2 ##### PROJETO ##########

# ARQUITETURA

                    RECICLACAMPUS
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
   ┌─────────────┐               ┌─────────────┐
   │  FRONT-END  │               │  BACK-END   │
   │    React    │◄──── API ────►│   Django    │
   └─────────────┘               └──────┬──────┘
                                        │
                                        ▼
                                ┌─────────────┐
                                │   BANCO     │
                                │ PostgreSQL  │
                                └─────────────┘

# FLUXOGRAMA
Usuário
   ↓
Login
   ↓
Encontra uma lixeira
   ↓
Escaneia o QR Code
   ↓
Seleciona o material
   ↓
Confirma o descarte
   ↓
Sistema calcula os pontos
   ↓
Pontos são adicionados ao usuário
   ↓
Ranking é atualizado

# BANCO DE DADOS 
┌──────────────┐
│   USUARIO    │
├──────────────┤
│ id           │
│ nome         │
│ email        │
│ senha        │
│ pontos       │
└──────┬───────┘
       │
       │ 1:N
       ▼
┌──────────────┐
│   DESCARTE   │
├──────────────┤
│ id           │
│ usuario_id   │
│ lixeira_id   │
│ material_id  │
│ pontos       │
│ data_hora    │
└───┬──────┬───┘
    │      │
    │      │
    ▼      ▼
┌────────┐ ┌──────────────┐
│MATERIAL│ │   LIXEIRA    │
├────────┤ ├──────────────┤
│ id     │ │ id           │
│ nome   │ │ codigo_qr    │
│ pontos │ │ localização  │
└────────┘ └──────────────┘


# CASOS DE USO
Ator: Usuário

Pode:
Criar conta;
Fazer login;
Visualizar pontos;
Escanear QR Code;
Registrar descarte;
Consultar histórico;
Visualizar ranking;
Consultar mapa.


Ator: Administrador
Pode:
Cadastrar lixeiras;
Gerenciar usuários;
Gerenciar materiais;
Criar campanhas;
Alterar pontuação;
Consultar descartes.


# PROTÓTIPO DE TELAS ##### FIGMA


##### FASE 3 ##### DESENVOLVIMENTO ###########

# TECNOLOGIAS
Back-end
Python
Django
Django REST Framework

Banco de dados
MySQL ou PostgreSQL

Front-end
React

Ferramentas
Git
GitHub
VS Code
Figma


# API
POST /api/login/
POST /api/usuarios/
GET  /api/usuarios/
GET  /api/ranking/
GET  /api/lixeiras/
POST /api/descartes/
GET  /api/descartes/

Depois podemos documentar cada endpoint:
Método	   Endpoint	         Função
POST	/api/descartes/	    Registrar descarte
GET	    /api/ranking/	    Consultar ranking
GET	    /api/lixeiras/	    Listar lixeiras
GET	    /api/descartes/  	Histórico de descartes


# GIT E ORGANIZAÇÃO DA EQUIPE

main
│
├── develop
│
├── feature/login
├── feature/ranking
├── feature/descartes
└── feature/lixeiras

###### FASE 4 ###### VALIDAÇÃO #########

# Testes

Documentar os testes realizados.

Exemplo:

Teste	                              Resultado esperado	     Resultado
Login com dados corretos          	 Usuário entra no sistema	    ✅
Login com senha incorreta    	     Sistema rejeita acesso	        ✅
Registro de descarte	             Pontos são adicionados	        ✅
QR Code inválido                   	 Sistema informa erro	        ✅
Ranking	Pontuação                    aparece corretamente           ✅

# RESULTADO 

# VALIDAÇÃO




 ##### FASE 5 ##### FINAL #####

# MANUAL 

# CONCLUSÃO 
O ReciclaCampus busca utilizar recursos tecnológicos e mecanismos de gamificação para estimular práticas sustentáveis dentro do ambiente universitário. Através do registro dos descartes, sistema de pontuação, ranking e localização das lixeiras, o projeto pretende tornar a reciclagem uma atividade mais acessível e estimulante para os estudantes.

# APRESENTAÇÃO
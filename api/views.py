from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Experimento 
from .serializers import ExperimentoSerializer 
from django.contrib.auth import authenticate, login 
from rest_framework.authtoken.models import Token 
from rest_framework import permissions, status

# View para listar (GET) e criar (POST)
class ExperimentoCreate(APIView):
    # Trata a requisição GET (Lista todos os experimentos)
    def get(self, request):
        experimentos = Experimento.objects.all()
        serializer = ExperimentoSerializer(experimentos, many=True) # 'many=True' indica uma lista
        return Response(serializer.data)

    # Trata a requisição POST (Cria um novo experimento)
    def post(self, request):
        serializer = ExperimentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

# View para detalhar (GET), editar (PUT/PATCH) e deletar (DELETE)
class ExperimentoDetalhe(APIView):
    # Trata a requisição GET (Retorna um experimento específico pelo PK)
    def get(self, request, pk):
        # Busca o objeto ou retorna 404 (Not Found)
        experimento = get_object_or_404(Experimento, pk=pk)
        serializer = ExperimentoSerializer(experimento)
        return Response(serializer.data)

class LoginView(APIView):
    # Define que esta View não requer autenticação para ser acessada (Permite o POST de credenciais)
    permission_classes = [permissions.AllowAny] 

    # Método POST: Responsável por receber o username/password e emitir o token de acesso
    def post(self, request, *args, **kwargs):
        # 1. Captura as credenciais enviadas na requisição JSON
        nome_usuario = request.data.get('username')
        senha = request.data.get('password')
        
        # 2. Tenta autenticar o usuário contra o banco de dados (sistema nativo Django)
        usuario_autenticado = authenticate(username=nome_usuario, password=senha)
        
        # 3. Verifica se a autenticação foi bem-sucedida (Se o usuário existe e a senha está correta)
        if usuario_autenticado is not None:
            # Realiza o login na sessão nativa do Django (opcional, mas mantido pelo tutorial)
            login(request, usuario_autenticado)
            
            # Cria ou obtém o Token DRF nativo (TokenAuthentication) para o usuário
            token_de_acesso, token_foi_criado_agora = Token.objects.get_or_create(user=usuario_autenticado) 
            
            # Retorna o token de acesso (a chave) para o Frontend (Ionic/Angular)
            # Status: HTTP 200 OK
            return Response({'message': 'Autenticação bem-sucedida no Gymbro! Treino liberado!',
                             'token': token_de_acesso.key}, 
                             status=status.HTTP_200_OK)
        else:
            # Retorna erro para credenciais inválidas (Usuário ou senha incorretos)
            # Status: HTTP 401 UNAUTHORIZED
            return Response({'error': 'Credenciais inválidas. Verifique seu usuário e senha.'}, 
                            status=status.HTTP_401_UNAUTHORIZED)
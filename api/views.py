# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from .models import Experimento, Cardio
from .serializers import ExperimentoSerializer, UserSerializer, CardioSerializer

# --- IMPORTS CRÍTICOS ---
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
# ------------------------

# --- VIEWS DE EXPERIMENTO ---

class ExperimentoCreate(APIView):
    def get(self, request):
        experimentos = Experimento.objects.all()
        serializer = ExperimentoSerializer(experimentos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperimentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class ExperimentoDetalhe(APIView):
    def get(self, request, pk):
        experimento = get_object_or_404(Experimento, pk=pk)
        serializer = ExperimentoSerializer(experimento)
        return Response(serializer.data)

# --- VIEWS DE AUTENTICAÇÃO ---

class LoginView(APIView):
    permission_classes = [permissions.AllowAny] 

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Autenticação bem-sucedida',
                'token': token.key 
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Credenciais inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request): 
        user_serializer = UserSerializer(data=request.data)
        try:
            if user_serializer.is_valid():
                user = user_serializer.save() 
                Token.objects.create(user=user)
                return Response(
                    {'message': 'Registro bem-sucedido'}, 
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'error': user_serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except IntegrityError as e:
            message = f"Erro ao registrar usuário: {e}"
            return Response(
                {'error': message}, 
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def api_testar_protecao(request):
    return Response(
        {'message': f"Acesso concedido à área protegida. Usuário autenticado: {request.user.username}"}, 
        status=status.HTTP_200_OK
    )

# --- VIEWS DE CARDIO (CORRIDA) ---

class CardioListCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Filtra cardios do usuário logado
        cardios = Cardio.objects.filter(usuario=request.user)
        serializer = CardioSerializer(cardios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CardioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CardioDetalhe(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def get_object(self, pk, user):
        return get_object_or_404(Cardio, pk=pk, usuario=user)

    def get(self, request, pk):
        cardio = self.get_object(pk, request.user)
        serializer = CardioSerializer(cardio)
        return Response(serializer.data)

    def put(self, request, pk):
        cardio = self.get_object(pk, request.user)
        serializer = CardioSerializer(cardio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cardio = self.get_object(pk, request.user)
        cardio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
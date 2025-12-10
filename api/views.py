from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Importe seus models e serializers
from .models import Experimento, UserProfile, Cardio, Exercicio, Ficha, ItemFicha
from .serializers import (
    ExperimentoSerializer, UserProfileSerializer, CardioSerializer, 
    ExercicioSerializer, FichaSerializer, ItemFichaSerializer, UserSerializer
)

# --- 1. Autenticação e Cadastro ---

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Libera pra quem não tem login
    serializer_class = UserSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
        
    # Rota mágica para o Frontend pegar o perfil sem saber o ID: /api/profiles/me/
    @action(detail=False, methods=['get'])
    def me(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

# --- 2. Sistema de Treinos (Gymbro) ---

class ExercicioViewSet(viewsets.ModelViewSet):
    serializer_class = ExercicioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retorna: Exercícios do Sistema (created_by=None) OU Exercícios do Próprio Usuário
        return Exercicio.objects.filter(
            Q(created_by__isnull=True) | Q(created_by=self.request.user)
        ).order_by('name')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class FichaViewSet(viewsets.ModelViewSet):
    serializer_class = FichaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ficha.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CardioViewSet(viewsets.ModelViewSet):
    serializer_class = CardioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cardio.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

# --- 3. Experimentos (Legado/Testes) ---

class ExperimentoCreate(APIView):
    permission_classes = [permissions.IsAuthenticated] # Agora exige login também
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
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        experimento = get_object_or_404(Experimento, pk=pk)
        serializer = ExperimentoSerializer(experimento)
        return Response(serializer.data)
    
class ItemFichaViewSet(viewsets.ModelViewSet):
    serializer_class = ItemFichaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Retorna apenas itens das fichas do usuário
        return ItemFicha.objects.filter(ficha__user=self.request.user)
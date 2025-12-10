from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExercicioViewSet, FichaViewSet, CardioViewSet, UserProfileViewSet, 
    RegisterView, ExperimentoCreate, ExperimentoDetalhe, ItemFichaViewSet,
)

# O Router cria as rotas padrão automaticamente
router = DefaultRouter()
router.register(r'exercicios', ExercicioViewSet, basename='exercicio')
router.register(r'fichas', FichaViewSet, basename='ficha')
router.register(r'cardio', CardioViewSet, basename='cardio')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'itens_ficha', ItemFichaViewSet, basename='item_ficha')

urlpatterns = [
    # Rotas do Router (Isso aqui gera /api/exercicios/, /api/fichas/, etc.)
    path('', include(router.urls)),
    
    # Rota de Cadastro
    path('registrar/', RegisterView.as_view(), name='auth_register'),
    
    # Rotas Antigas (Experimentos)
    path('experimentos/', ExperimentoCreate.as_view(), name='experimento-create'),
    path('experimentos/<int:pk>/', ExperimentoDetalhe.as_view(), name='experimento-detalhe'),
]
# api/urls.py

from django.urls import path
from .views import (ExperimentoCreate, ExperimentoDetalhe, CardioListCreate, CardioDetalhe, ExercicioListCreate, FichaListCreate, ItemFichaCreate)

urlpatterns = [
    # --- EXPERIMENTOS (Legado/Teste) ---
    path('experimentos/', ExperimentoCreate.as_view(), name='experimento-create'),
    path('experimentos/<int:pk>/', ExperimentoDetalhe.as_view(), name='experimento-detalhe'),
    
    # --- CARDIO (Corridas com GPS) ---
    path('cardios/', CardioListCreate.as_view(), name='cardio-list-create'),
    path('cardios/<int:pk>/', CardioDetalhe.as_view(), name='cardio-detalhe'),

    # --- EXERCÍCIOS (Catálogo Global + Customizados) ---
    # GET: Lista todos (globais + meus). POST: Cria um customizado.
    path('exercicios/', ExercicioListCreate.as_view(), name='exercicio-list-create'),
    
    # --- FICHAS DE TREINO ---
    # GET: Lista minhas fichas. POST: Cria nova ficha.
    path('fichas/', FichaListCreate.as_view(), name='ficha-list-create'),
    
    # --- ITENS DA FICHA (Montagem do Treino) ---
    # POST: Adiciona um exercício dentro de uma ficha específica
    path('fichas/<int:ficha_id>/itens/', ItemFichaCreate.as_view(), name='item-ficha-create'),
]
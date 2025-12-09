from .views import ExperimentoCreate, ExperimentoDetalhe 
from django.urls import path

urlpatterns = [
    # Rota para listar (GET) e criar (POST) experimentos
    path('experimentos/', ExperimentoCreate.as_view(), name='experimento-create'),
    
    # Rota para detalhar (GET) experimentos com uma chave primária (PK)
    path('experimentos/<int:pk>/', ExperimentoDetalhe.as_view(), name='experimento-detalhe'),
]

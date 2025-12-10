from django.urls import path
from .views import ExperimentoCreate, ExperimentoDetalhe, CardioListCreate, CardioDetalhe
urlpatterns = [
    # Rotas de Experimento
    path('experimentos/', ExperimentoCreate.as_view(), name='experimento-create'),
    path('experimentos/<int:pk>/', ExperimentoDetalhe.as_view(), name='experimento-detalhe'),
    
    # Expondo a rota para listar e criar cardios (GET e POST)
    path('cardios/', CardioListCreate.as_view(), name='cardio-list-create'),
    # --- NOVA ROTA DE DETALHE/EDIÇÃO/REMOÇÃO ---
    path('cardios/<int:pk>/', CardioDetalhe.as_view(), name='cardio-detalhe'),
]
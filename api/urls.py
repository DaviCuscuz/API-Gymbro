from .views import ExperimentoCreate, ExperimentoDetalhe 
from django.urls import path

urlpatterns = [
    path('experimentos/', ExperimentoCreate.as_view(), name='experimento-create'),
    
    path('experimentos/<int:pk>/', ExperimentoDetalhe.as_view(), name='experimento-detalhe'),
]

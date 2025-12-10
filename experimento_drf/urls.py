from django.contrib import admin
from django.urls import path, include
from api.views import LoginView, RegisterView, api_testar_protecao 
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Rotas de Autenticação do Gymbro
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    
    # --- NOVA ROTA PROTEGIDA PARA TESTE ---
    path('api/protegida/', api_testar_protecao, name='api_protegida'),
]

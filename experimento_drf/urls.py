from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # <--- 1. Importe isso aqui

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 2. Essa linha mágica joga quem acessar o site puro direto pra API
    path('', RedirectView.as_view(url='/api/', permanent=False)),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Rotas JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
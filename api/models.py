# api/models.py

from django.db import models
from django.contrib.auth.models import User

# --- 1. Model de Experimento (Teste Inicial) ---
class Experimento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

# --- 2. Model de Perfil (Segurança e Dados Pessoais) ---
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campos protegidos com unique=True (Blindagem do Banco)
    email = models.EmailField(max_length=254, unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    
    nome_completo = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

# --- 3. Model de Cardio (Nova Funcionalidade de Corrida) ---
class Cardio(models.Model):
    """
    Model para registrar sessões de cardio (Corrida)
    Armazena dados de uma única sessão de corrida com rota GPS
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessoes_cardio')
    distancia = models.FloatField(help_text="Distância em quilômetros (km)")
    
    # DurationField é perfeito para cronômetros (armazena 'HH:MM:SS')
    tempo = models.DurationField(help_text="Tempo total da sessão")
    
    data_hora = models.DateTimeField(auto_now_add=True)
    
    # JSONField: Aqui o Ionic vai mandar o array de coordenadas [lat, lng]
    rota_gps = models.JSONField(default=dict, blank=True, help_text="Dados da rota GPS em formato JSON")
    
    calorias_queimadas = models.FloatField(null=True, blank=True, help_text="Calorias estimadas queimadas")
    velocidade_media = models.FloatField(null=True, blank=True, help_text="Velocidade média em km/h")
    
    class Meta:
        ordering = ['-data_hora']
        verbose_name = 'Sessão de Cardio'
        verbose_name_plural = 'Sessões de Cardio'
    
    def __str__(self):
        # Formata a data para ficar legível no Admin
        return f"Corrida - {self.usuario.username} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
    
    def calcular_velocidade_media(self):
        """Calcula a velocidade média em km/h automaticamente"""
        if self.tempo.total_seconds() > 0:
            horas = self.tempo.total_seconds() / 3600
            self.velocidade_media = self.distancia / horas
            return self.velocidade_media
        return 0
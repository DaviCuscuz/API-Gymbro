from django.db import models
from django.contrib.auth.models import User

# --- 1. Experimento, UserProfile, Cardio
class Experimento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.titulo

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    nome_completo = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    # Campos de Medidas
    altura = models.FloatField(null=True, blank=True, help_text="Altura em cm")
    peso = models.FloatField(null=True, blank=True, help_text="Peso em kg")
    def __str__(self):
        return self.user.username

class Cardio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessoes_cardio')
    distancia = models.FloatField(help_text="Distância em km")
    tempo = models.DurationField(help_text="Tempo total")
    data_hora = models.DateTimeField(auto_now_add=True)
    rota_gps = models.JSONField(default=dict, blank=True)
    calorias_queimadas = models.FloatField(null=True, blank=True)
    velocidade_media = models.FloatField(null=True, blank=True)
    class Meta: ordering = ['-data_hora']
    def __str__(self): return f"Corrida - {self.usuario.username}"
    def calcular_velocidade_media(self):
        if self.tempo.total_seconds() > 0:
            horas = self.tempo.total_seconds() / 3600
            self.velocidade_media = self.distancia / horas
            return self.velocidade_media
        return 0

# --- CONSTANTES ---
TIPO_MOVIMENTO = [
    ('EMPURRAR', 'Empurrar'), ('PUXAR', 'Puxar'),
    ('INFERIOR', 'Inferior (Pernas)'), ('CORE', 'Core'),
    ('MOBILIDADE', 'Mobilidade/Aquecimento'),
]
NIVEL_DIFICULDADE = [
    ('INICIANTE', 'Iniciante'), ('INTERMEDIARIO', 'Intermediário'),
    ('AVANCADO', 'Avançado'), ('EXPERT', 'Expert'),
]

# --- 2. Exercicio 
class Exercicio(models.Model):
    # Se created_by for NULL, é Global. Se tiver User, é Customizado.
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='custom_exercises',
        verbose_name="Criado por (Customizado)"
    )
    
    name = models.CharField(max_length=100, verbose_name="Nome") 
    description = models.TextField(blank=True, verbose_name="Instruções")
    
    tipo_movimento = models.CharField(max_length=20, choices=TIPO_MOVIMENTO, default='EMPURRAR')
    nivel_dificuldade = models.CharField(max_length=20, choices=NIVEL_DIFICULDADE, default='INICIANTE')

    def __str__(self):
        origem = "Custom" if self.created_by else "Global"
        return f"{self.name} ({origem})"
    
    class Meta:
        verbose_name = "Exercício"
        verbose_name_plural = "Catálogo de Exercícios"
        ordering = ['name']

# --- 3. Ficha e ItemFicha
class Ficha(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    name = models.CharField(max_length=100, verbose_name="Nome da Ficha")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.name} ({self.user.username})"

class ItemFicha(models.Model):
    ficha = models.ForeignKey(Ficha, related_name='items', on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.PROTECT)
    sets = models.IntegerField(default=3)
    repetitions = models.CharField(max_length=50, blank=True, null=True)
    tempo_segundos = models.IntegerField(default=0)
    peso_adicional_kg = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    order = models.IntegerField(default=0)
    def __str__(self): return f"{self.exercicio.name} na ficha {self.ficha.name}"
    class Meta: ordering = ['order']
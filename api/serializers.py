from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Experimento, UserProfile, Cardio, Exercicio, Ficha, ItemFicha

# --- 1. Serializers de Experimento (Teste Inicial)
class ExperimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experimento
        fields = '__all__'

# --- 2. Serializers de Autenticação (User + Profile) 
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'nome_completo', 'endereco', 'cidade', 'estado', 'telefone', 'cpf', 'altura', 'peso']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password', None)
        
        try:
            user = User.objects.create(**validated_data)
            if password:
                user.set_password(password)
                user.save()
            UserProfile.objects.create(user=user, **profile_data)
            return user
        except IntegrityError as e:
            raise serializers.ValidationError(f"Erro ao registrar usuário: {e}")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile_instance = instance.userprofile
        
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        
        profile_instance.email = profile_data.get('email', profile_instance.email)
        profile_instance.nome_completo = profile_data.get('nome_completo', profile_instance.nome_completo)
        profile_instance.endereco = profile_data.get('endereco', profile_instance.endereco)
        profile_instance.cidade = profile_data.get('cidade', profile_instance.cidade)
        profile_instance.estado = profile_data.get('estado', profile_instance.estado)
        profile_instance.telefone = profile_data.get('telefone', profile_instance.telefone)
        profile_instance.cpf = profile_data.get('cpf', profile_instance.cpf)
        profile_instance.save()
        return instance

# --- 3. Serializer de Cardio (Corrida) ---
class CardioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardio
        fields = '__all__'
        read_only_fields = ['usuario']

# --- 4. Serializers de Treino (Exercicio, Ficha, Item) ---

class ExercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercicio
        fields = '__all__'
        read_only_fields = ['created_by'] 

class ItemFichaSerializer(serializers.ModelSerializer):
    exercicio_detalhes = ExercicioSerializer(source='exercicio', read_only=True)
    exercicio_id = serializers.PrimaryKeyRelatedField(
        queryset=Exercicio.objects.all(), source='exercicio', write_only=True
    )
    ficha_id = serializers.PrimaryKeyRelatedField(
        queryset=Ficha.objects.all(), source='ficha', write_only=True
    )

    class Meta:
        model = ItemFicha
        fields = [
            'id', 
            'ficha_id',          
            'exercicio_id',      
            'exercicio_detalhes',
            'sets', 
            'repetitions', 
            'tempo_segundos', 
            'peso_adicional_kg', 
            'order'
        ]

class FichaSerializer(serializers.ModelSerializer):
    items = ItemFichaSerializer(many=True, read_only=True)

    class Meta:
        model = Ficha
        fields = ['id', 'name', 'is_active', 'created_at', 'items']
        read_only_fields = ['user']

class RegisterSerializer(serializers.ModelSerializer):
    # Definimos explicitamente para aceitar 'email' e 'password' no nível raiz
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # 1. Separa os dados
        email = validated_data.get('email', '')
        username = validated_data['username']
        password = validated_data['password']

        # 2. Cria o Usuário (com senha criptografada)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 3. Cria o Perfil automaticamente (Já que removemos os signals)
        # Repassamos o email para o perfil também
        UserProfile.objects.create(user=user, email=email)

        return user
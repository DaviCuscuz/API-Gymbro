from rest_framework import serializers
from .models import Experimento, UserProfile, Cardio 
from django.contrib.auth.models import User
from django.db import IntegrityError 

# Seu Serializer original
class ExperimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experimento
        fields = '__all__' 

# 1. Serializer para o modelo de perfil de usuário (Conforme PDF, pág. 33)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # Campos que o Front-end deve enviar para o perfil
        fields = ['id', 'email', 'nome_completo', 'endereco', 'cidade', 'estado', 'telefone', 'cpf']

# 2. Serializer principal (aninhado) com lógica de criação (Conforme PDF, pág. 34)
class UserSerializer(serializers.ModelSerializer):
    # Relaciona o UserProfileSerializer como um campo aninhado 'profile'
    profile = UserProfileSerializer() 

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'profile']
        # Garante que a senha seja 'write_only', nunca retornada em um GET
        extra_kwargs = {'password': {'write_only': True}} 

    # Sobrescreve o método 'create' para tratar a senha e o perfil
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password', None)
        
        try:
            # Cria o usuário padrão do Django
            user = User.objects.create(**validated_data)
            
            # Se houver senha, salva ela criptografada (set_password é crucial)
            if password:
                user.set_password(password)
                user.save()

            # Cria a instância do UserProfile, vinculando ao novo usuário
            UserProfile.objects.create(user=user, **profile_data)
            return user
            
        except IntegrityError as e:
            # Lança um erro de validação caso algo dê errado no banco (ex: username duplicado)
            message = f"Erro ao registrar usuário: {e}"
            raise serializers.ValidationError(message)
    
    # O método 'update' (pág. 35 do PDF) para editar o usuário/perfil
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        # O nome do atributo é 'userprofile' por ser um OneToOneField no UserProfile
        profile_instance = instance.userprofile 
        
        # Atualiza campos do User
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        
        # Atualiza campos do UserProfile (pág. 35 do PDF)
        profile_instance.email = profile_data.get('email', profile_instance.email)
        profile_instance.nome_completo = profile_data.get('nome_completo', profile_instance.nome_completo)
        profile_instance.endereco = profile_data.get('endereco', profile_instance.endereco)
        profile_instance.cidade = profile_data.get('cidade', profile_instance.cidade)
        profile_instance.estado = profile_data.get('estado', profile_instance.estado)
        profile_instance.telefone = profile_data.get('telefone', profile_instance.telefone)
        profile_instance.cpf = profile_data.get('cpf', profile_instance.cpf)
        profile_instance.save()

        return instance

class CardioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardio
        fields = '__all__'
        # O campo usuario será preenchido automaticamente pela View usando o Token
        read_only_fields = ['usuario']
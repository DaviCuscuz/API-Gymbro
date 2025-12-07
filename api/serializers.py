from rest_framework import serializers
from .models import Experimento 

class ExperimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experimento
        fields = '__all__' 
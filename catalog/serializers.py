from rest_framework import serializers
from .models import *

class MiModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiModelo
        fields = ['id', 'campo1', 'campo2']

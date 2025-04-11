from rest_framework import serializers
from enderecos.models import Endereco
from usuarios.models import Usuario

class EnderecoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Usuario.objects.all())
    class Meta:
        model = Endereco
        fields = '__all__'
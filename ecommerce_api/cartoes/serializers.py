from rest_framework import serializers
from cartoes.models import CartaoCredito
from usuarios.models import Usuario

class CartaoCreditoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    class Meta:
        model = CartaoCredito
        fields = '__all__'  # Inclui todos os campos do modelo Cartao

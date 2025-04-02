from rest_framework import serializers
from cartoes.models import CartaoCredito

class CartaoCreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaoCredito
        fields = '__all__'  # Inclui todos os campos do modelo Cartao

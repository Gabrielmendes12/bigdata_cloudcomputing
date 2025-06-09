from rest_framework import serializers

class PedidoSerializer(serializers.Serializer):
    # campos que o bot envia após uma compra realizada
    produto_id = serializers.CharField()
    numero_cartao = serializers.CharField()
    # campos de resposta no backend
    id = serializers.CharField(read_only=True)
    valor = serializers.FloatField(read_only=True)
    id_pedidousuario = serializers.CharField(read_only=True)
    data_pedido = serializers.DateTimeField(read_only=True)

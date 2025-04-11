from rest_framework import serializers

class ProdutoSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nome = serializers.CharField()
    descricao = serializers.CharField()
    preco = serializers.FloatField()
    categoria = serializers.CharField()
    imagem_url = serializers.URLField()


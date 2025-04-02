from django.db import models

# Create your models here.
class Produto(models.Model):
    id_produto = models.UUIDField(primary_key=True, editable=False, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    categoria = models.CharField(max_length=50, default='Geral')
    imagem_url = models.URLField(default='https://example.com/imagem.jpg')
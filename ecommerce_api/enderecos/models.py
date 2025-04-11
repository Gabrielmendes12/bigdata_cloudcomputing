from django.db import models

# Create your models here.
class Endereco(models.Model):
    id_endereco = models.AutoField(primary_key=True, db_column="id")  # AUTO_INCREMENT no MySQL
    logradouro = models.CharField(max_length=200, null=True, db_column="logradouro")
    complemento = models.CharField(max_length=200, null=True, blank=True, db_column="complemento")
    bairro = models.CharField(max_length=100, null=True, db_column="bairro")
    cidade = models.CharField(max_length=100, null=True, db_column="cidade")
    estado = models.CharField(max_length=100, null=True, db_column="estado")
    #tipo = models.CharField(max_length=45, null=True, db_column="tipo")  # <-- campo direto
    
    usuario = models.ForeignKey(
        "usuarios.Usuario", null=True, on_delete=models.CASCADE, db_column="id_usuario" 
    ) # estava SET_NULL, mas o correto é CASCADE, pois se o usuário for excluído, os endereços também devem ser excluídos?

    class Meta:
        db_table = "endereco"
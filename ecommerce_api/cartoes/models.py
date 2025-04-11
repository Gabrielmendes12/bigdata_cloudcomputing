from django.db import models

# Create your models here.
class CartaoCredito(models.Model):
    id_cartao = models.AutoField(primary_key=True, db_column="id")  # AUTO_INCREMENT no MySQL
    numero = models.CharField(max_length=45, null=True, db_column="numero")
    data_expiracao = models.DateTimeField(null=True, db_column="dtExpiracao")  # DATETIME no MySQL
    cvv = models.CharField(max_length=3, null=True, db_column="cvv")
    saldo = models.FloatField(null=True, db_column="saldo")
    usuario = models.ForeignKey(
        "usuarios.Usuario", null=True, on_delete=models.CASCADE, db_column="id_usuario_cartao"
    ) # estava SET_NULL, mas o correto é CASCADE, pois se o usuário for excluído, os cartões também devem ser excluídos

    class Meta:
        db_table = "cartao_credito"


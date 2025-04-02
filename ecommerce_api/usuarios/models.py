from django.db import models

# Create your models here.
class Usuario(models.Model):
    # Dados pessoais
    id = models.AutoField(primary_key=True, db_column="id")  # AUTO_INCREMENT no MySQL
    nome = models.CharField(max_length=100, null=True, db_column="nome")
    email = models.EmailField(null=True, db_column="email")
    cpf = models.CharField(max_length=11, unique=True, db_column="CPF")
    data_nascimento = models.DateTimeField(null=True, db_column="dtNascimento")  # DATETIME no MySQL
    telefone = models.CharField(max_length=20, null=True, db_column="Telefone")

    class Meta:
        db_table = "usuario"
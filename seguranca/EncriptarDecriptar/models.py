from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField('nome', max_length=100)
    email = models.CharField('email', max_length=100)
    chave = models.CharField('chave', max_length=200, null=True)
    user = models.ForeignKey(User)

class Mensagem(models.Model):
    mensagem = models.TextField('mensagem')
    usuario = models.ForeignKey(Usuario)
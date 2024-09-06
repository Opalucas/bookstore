from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)
    data_publicacao = models.DateField()
    capa = models.URLField()  # URL para a capa do livro
    sinopse = models.TextField()
    paginas = models.IntegerField()
    publicadora = models.CharField(max_length=255)

class Cart(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livros = models.ManyToManyField(Book)
    data_criacao = models.DateTimeField(auto_now_add=True)

class Sel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livros = models.ManyToManyField(Book)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateTimeField(auto_now_add=True)
    

class Addres(models.Model):
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    cep = models.CharField(max_length=10)
        

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    addres = models.ForeignKey(Addres, on_delete=models.CASCADE)
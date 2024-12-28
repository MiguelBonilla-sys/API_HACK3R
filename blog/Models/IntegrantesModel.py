from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from cloudinary.models import CloudinaryField

class Integrantes(models.Model):
    idintegrantes = models.AutoField(primary_key=True)
    nombre_integrante = models.CharField(max_length=220)
    semestre = models.CharField(max_length=50)
    correo = models.CharField(max_length=550)
    link_git = models.CharField(max_length=650)
    imagen = CloudinaryField('image', folder='integrantes/')
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.BooleanField()
    reseña = models.TextField()

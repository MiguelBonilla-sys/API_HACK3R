from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Integrantes(models.Model):
    idintegrantes = models.AutoField(primary_key=True)
    nombre_integrante = models.CharField(max_length=220)
    semestre = models.CharField(max_length=50)
    correo = models.CharField(max_length=550)
    link_git = models.CharField(max_length=650)
    imagen = models.TextField(
            validators=[
                RegexValidator(
                    regex=r'^data:image/[a-zA-Z]+;base64,',  # Usando raw string
                    message='La imagen debe estar en formato base64',
                    code='invalid_image'
                )
            ]
        )
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.BooleanField()
    reseña = models.TextField()

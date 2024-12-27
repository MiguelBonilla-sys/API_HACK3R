from django.db import models
from django.contrib.auth.models import User

class Conferencias(models.Model):
    idconferencia = models.AutoField(primary_key=True)
    nombre_conferencia = models.CharField(max_length=620)
    ponente_conferencia = models.CharField(max_length=250)
    fecha_conferencia = models.DateTimeField(blank=True, null=True)
    descripcion_conferencia = models.CharField(max_length=1200)
    imagen_conferencia = models.ImageField(upload_to='img/conferencias/')
    link_conferencia = models.CharField(max_length=1200)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
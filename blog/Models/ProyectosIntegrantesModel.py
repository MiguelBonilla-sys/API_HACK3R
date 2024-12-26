from django.db import models
from blog.Models.IntegrantesModel import Integrantes
from blog.Models.ProyectosModel import Proyectos

class ProyectosIntegrantesProyecto(models.Model):
    proyectos = models.OneToOneField(Proyectos, on_delete=models.CASCADE, primary_key=True)
    integrantes = models.ForeignKey(Integrantes, on_delete=models.CASCADE)

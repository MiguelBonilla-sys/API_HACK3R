from django.db import models
from django.contrib.auth.models import User

class Cursos(models.Model):
    idcursos = models.AutoField(primary_key=True)  # Field name made lowercase.
    nombre_curso = models.CharField(max_length=120)  # Field name made lowercase.
    fechainicial_curso = models.DateTimeField(null=True, blank=True)  # Field name made lowercase.
    fechafinal_curso = models.DateTimeField(null=True, blank=True)  # Field name made lowercase.
    link_curso = models.CharField(max_length=1200)  # Field name made lowercase.
    descripcion_curso = models.CharField(max_length=1200)  # Field name made lowercase.
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

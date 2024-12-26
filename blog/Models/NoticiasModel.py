from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Noticias(models.Model):
    idnoticia = models.AutoField(primary_key=True)  # Field name made lowercase.
    nombre_noticia = models.CharField(max_length=600)  # Field name made lowercase.
    fecha_noticia = models.DateTimeField()  # Field name made lowercase.
    link_noticia = models.CharField(max_length=250)  # Field name made lowercase.
    description_noticia = models.CharField(max_length=1450)  # Field name made lowercase.
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    fuente = models.CharField(max_length=250, blank=True, null=True)
    imagen_noticia = models.TextField(
            validators=[
                RegexValidator(
                    regex=r'^data:image/[a-zA-Z]+;base64,',  # Usando raw string
                    message='La imagen debe estar en formato base64',
                    code='invalid_image'
                )
            ]
        )


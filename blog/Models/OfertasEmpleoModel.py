from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.core.validators import RegexValidator

class OfertasEmpleo(models.Model):
    idoferta = models.AutoField(primary_key=True)
    titulo_empleo = models.CharField(max_length=620)
    empresa = models.CharField(max_length=230)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    descripcion_empleo = models.CharField(max_length=1200)
    imagen = models.TextField()
    link_oferta = models.TextField(
            validators=[
                RegexValidator(
                    regex=r'^data:image/[a-zA-Z]+;base64,',  # Usando raw string
                    message='La imagen debe estar en formato base64',
                    code='invalid_image'
                )
            ]
        )
    fecha_expiracion = models.DateTimeField(blank=True, null=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:  # Si el objeto es nuevo
            self.fecha_publicacion = timezone.now()
        if not self.fecha_expiracion:
            self.fecha_expiracion = self.fecha_publicacion + timedelta(days=60)  # Por ejemplo, 60 días después de la creación
        super(OfertasEmpleo, self).save(*args, **kwargs)

    def __str__(self):
        return self.creador.username
    
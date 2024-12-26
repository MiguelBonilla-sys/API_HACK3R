from celery import shared_task
from django.utils import timezone
from blog.Models.OfertasEmpleoModel import OfertasEmpleo

@shared_task
def eliminar_ofertas_expiradas():
    ahora = timezone.now()
    OfertasEmpleo.objects.filter(fecha_expiracion__lt=ahora).delete()
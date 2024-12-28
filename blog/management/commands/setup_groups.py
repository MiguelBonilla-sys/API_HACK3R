from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from blog.Models.CursosModel import Cursos
from blog.Models.IntegrantesModel import Integrantes
from blog.Models.ProyectosModel import Proyectos
from blog.Models.NoticiasModel import Noticias
from blog.Models.AuditLogModel import AuditLog
from blog.Models.ConferenciasModel import Conferencias
from blog.Models.OfertasEmpleoModel import OfertasEmpleo

class Command(BaseCommand):
    help = 'Setup groups and permissions'

    def handle(self, *args, **kwargs):
        # Crear grupos
        staff_group, created = Group.objects.get_or_create(name='Staff')
        admin_group, created = Group.objects.get_or_create(name='Admin')

        # Obtener permisos
        content_type = ContentType.objects.get_for_model(User)
        try:
            add_user_permission = Permission.objects.get(codename='add_user', content_type=content_type)
        except Permission.DoesNotExist:
            add_user_permission = Permission.objects.create(codename='add_user', name='Can add user', content_type=content_type)

        try:
            change_user_permission = Permission.objects.get(codename='change_user', content_type=content_type)
        except Permission.DoesNotExist:
            change_user_permission = Permission.objects.create(codename='change_user', name='Can change user', content_type=content_type)

        # Asignar permisos al grupo de staff
        staff_group.permissions.add(change_user_permission)

        models_to_assign = [Cursos, Integrantes, Noticias, Proyectos, AuditLog, Conferencias, OfertasEmpleo]
        for model in models_to_assign:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                if perm.codename in ['add', 'change', 'delete', 'view']:
                    staff_group.permissions.add(perm)
                    admin_group.permissions.add(perm)

        # Asignar todos los permisos al grupo de admin
        admin_group.permissions.set(Permission.objects.all())

        # Configurar la tarea periódica para que se ejecute diariamente
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )

        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Eliminar ofertas expiradas',
            task='blog.tasks.eliminar_ofertas_expiradas',
        )
        
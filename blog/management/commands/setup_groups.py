# blog/management/commands/setup_groups.py

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
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Configura grupos y permisos del sistema'

    def handle(self, *args, **kwargs):
        self.stdout.write('Configurando grupos y permisos...')
        
        # Crear o actualizar grupos principales
        staff_group = self._create_or_update_group('Staff')
        editor_group = self._create_or_update_group('Editor')
        viewer_group = self._create_or_update_group('Viewer')
        
        # Modelos que manejaremos
        models_to_handle = [
            Cursos, 
            Integrantes, 
            Noticias, 
            Proyectos, 
            AuditLog, 
            Conferencias, 
            OfertasEmpleo
        ]
        
        # Configurar permisos por grupo
        self._setup_staff_permissions(staff_group, models_to_handle)
        self._setup_editor_permissions(editor_group, models_to_handle)
        self._setup_viewer_permissions(viewer_group, models_to_handle)
        
        # Configurar tarea periódica
        self._setup_periodic_task()
        
        self.stdout.write(self.style.SUCCESS('Grupos y permisos configurados exitosamente'))
    
    def _create_or_update_group(self, name):
        """Crea o actualiza un grupo."""
        group, created = Group.objects.get_or_create(name=name)
        action = 'Creado' if created else 'Actualizado'
        self.stdout.write(f'{action} grupo {name}')
        return group
    
    def _setup_staff_permissions(self, group, models):
        """Configura permisos para el grupo Staff."""
        # Staff tiene todos los permisos en todos los modelos
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            group.permissions.add(*permissions)
            
        self.stdout.write(f'Configurados permisos de Staff')
    
    def _setup_editor_permissions(self, group, models):
        """Configura permisos para el grupo Editor."""
        # Editores pueden ver, agregar y modificar, pero no eliminar
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            
            # Excluir AuditLog para editores
            if model != AuditLog:
                permissions = Permission.objects.filter(
                    content_type=content_type,
                    codename__in=[
                        f'view_{model._meta.model_name}',
                        f'add_{model._meta.model_name}',
                        f'change_{model._meta.model_name}'
                    ]
                )
                group.permissions.add(*permissions)
            
        self.stdout.write(f'Configurados permisos de Editor')
    
    def _setup_viewer_permissions(self, group, models):
        """Configura permisos para el grupo Viewer."""
        # Viewers solo pueden ver
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            
            # Excluir AuditLog para viewers
            if model != AuditLog:
                permission = Permission.objects.get(
                    content_type=content_type,
                    codename=f'view_{model._meta.model_name}'
                )
                group.permissions.add(permission)
            
        self.stdout.write(f'Configurados permisos de Viewer')
    
    def _setup_periodic_task(self):
        """Configura la tarea periódica de limpieza."""
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )
        
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Eliminar ofertas expiradas',
            task='blog.tasks.eliminar_ofertas_expiradas',
        )
        
        self.stdout.write('Configurada tarea periódica')
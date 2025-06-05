"""
ViewSet base con funcionalidad común para todos los modelos.

Este módulo proporciona un ViewSet base que incluye:
- Verificación de permisos
- Logging de acciones
- Manejo de errores común
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from blog.services.permissions_service import check_model_permission
import logging

logger = logging.getLogger(__name__)

class BaseModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base con funcionalidad común para todos los modelos.
    
    Incluye:
    - Verificación automática de permisos
    - Configuración estándar de filtros y paginación
    - Manejo de errores común
    - Logging de acciones
    """
    
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get_model_name(self):
        """Obtiene el nombre del modelo en minúsculas."""
        return self.queryset.model._meta.model_name
    
    def check_object_permissions(self, request, obj):
        """
        Verifica permisos específicos para el objeto.
        
        Args:
            request: Request actual
            obj: Objeto a verificar
        """
        super().check_object_permissions(request, obj)
        
        # Verificar si el usuario es el creador (si aplica)
        if hasattr(obj, 'creador') and obj.creador != request.user:
            if not request.user.is_staff:
                self.permission_denied(
                    request,
                    message='No tienes permiso para modificar este objeto'
                )
    
    def check_action_permission(self, request, action):
        """
        Verifica si el usuario tiene permiso para realizar la acción.
        
        Args:
            request: Request actual
            action: Acción a verificar (view, add, change, delete)
        """
        model_name = self.get_model_name()
        has_perm = check_model_permission(request.user, model_name, action)
        
        if not has_perm:
            self.permission_denied(
                request,
                message=f'No tienes permiso para {action} {model_name}'
            )
    
    def list(self, request, *args, **kwargs):
        """Lista objetos verificando permisos."""
        self.check_action_permission(request, 'view')
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Crea un objeto verificando permisos."""
        self.check_action_permission(request, 'add')
        return super().create(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """Obtiene un objeto verificando permisos."""
        self.check_action_permission(request, 'view')
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """Actualiza un objeto verificando permisos."""
        self.check_action_permission(request, 'change')
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Actualiza parcialmente un objeto verificando permisos."""
        self.check_action_permission(request, 'change')
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Elimina un objeto verificando permisos."""
        self.check_action_permission(request, 'delete')
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """
        Crea un objeto asignando el usuario actual como creador.
        
        Args:
            serializer: Serializer con los datos validados
        """
        if hasattr(serializer.Meta.model, 'creador'):
            serializer.save(creador=self.request.user)
        else:
            serializer.save()
            
        logger.info(
            f"Usuario {self.request.user} creó {self.get_model_name()} "
            f"ID={serializer.instance.pk}"
        )
    
    def perform_update(self, serializer):
        """
        Actualiza un objeto registrando la acción.
        
        Args:
            serializer: Serializer con los datos validados
        """
        super().perform_update(serializer)
        logger.info(
            f"Usuario {self.request.user} actualizó {self.get_model_name()} "
            f"ID={serializer.instance.pk}"
        )
    
    def perform_destroy(self, instance):
        """
        Elimina un objeto registrando la acción.
        
        Args:
            instance: Instancia a eliminar
        """
        pk = instance.pk
        super().perform_destroy(instance)
        logger.info(
            f"Usuario {self.request.user} eliminó {self.get_model_name()} "
            f"ID={pk}"
        ) 
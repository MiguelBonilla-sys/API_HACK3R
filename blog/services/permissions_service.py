"""
Servicio para gestionar permisos y grupos de usuarios.

Este módulo proporciona funciones para gestionar permisos de usuario
y sincronizar los permisos entre Django Admin y el frontend.
"""

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def get_user_permissions(user: User) -> Dict[str, Dict[str, bool]]:
    """
    Obtiene todos los permisos del usuario para cada modelo.
    
    Args:
        user: Usuario del cual obtener los permisos
        
    Returns:
        Dict con permisos por modelo:
        {
            'modelo': {
                'view': bool,
                'add': bool,
                'change': bool,
                'delete': bool
            }
        }
    """
    if not user.is_authenticated:
        return {}
        
    # Modelos disponibles en la aplicación
    app_models = [
        'auditlog',
        'conferencias', 
        'cursos',
        'integrantes',
        'noticias',
        'ofertasempleo',
        'proyectos'
    ]
    
    permissions = {}
    
    for model in app_models:
        model_perms = {
            'view': user.has_perm(f'blog.view_{model}'),
            'add': user.has_perm(f'blog.add_{model}'),
            'change': user.has_perm(f'blog.change_{model}'),
            'delete': user.has_perm(f'blog.delete_{model}')
        }
        permissions[model] = model_perms
        
    return permissions

def get_user_groups(user: User) -> List[str]:
    """
    Obtiene los grupos a los que pertenece el usuario.
    
    Args:
        user: Usuario del cual obtener los grupos
        
    Returns:
        Lista de nombres de grupos
    """
    return list(user.groups.values_list('name', flat=True))

def get_all_permissions() -> Dict[str, List[str]]:
    """
    Obtiene todos los permisos disponibles agrupados por modelo.
    
    Returns:
        Dict con permisos agrupados por modelo
    """
    app_permissions = {}
    
    content_types = ContentType.objects.filter(app_label='blog')
    
    for ct in content_types:
        model_perms = Permission.objects.filter(content_type=ct)
        app_permissions[ct.model] = [
            {
                'id': perm.pk,
                'codename': perm.codename,
                'name': perm.name
            }
            for perm in model_perms
        ]
        
    return app_permissions

def get_group_permissions(group_name: str) -> Dict[str, List[str]]:
    """
    Obtiene los permisos asignados a un grupo específico.
    
    Args:
        group_name: Nombre del grupo
        
    Returns:
        Dict con permisos del grupo por modelo
    """
    try:
        group = Group.objects.get(name=group_name)
        permissions = {}
        
        for perm in group.permissions.all():
            model = perm.content_type.model
            if model not in permissions:
                permissions[model] = []
            permissions[model].append(perm.codename)
            
        return permissions
        
    except Group.DoesNotExist:
        logger.warning(f"Grupo {group_name} no encontrado")
        return {}

def check_model_permission(user: User, model: str, action: str) -> bool:
    """
    Verifica si un usuario tiene un permiso específico sobre un modelo.
    
    Args:
        user: Usuario a verificar
        model: Nombre del modelo
        action: Acción a verificar (view, add, change, delete)
        
    Returns:
        bool indicando si tiene el permiso
    """
    if not user.is_authenticated:
        return False
        
    permission = f'blog.{action}_{model}'
    return user.has_perm(permission) 
"""
API Views para gestión de permisos de usuario.

Este módulo proporciona endpoints para consultar y verificar
permisos de usuario en tiempo real.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import logging

from blog.services.permissions_service import (
    get_user_permissions,
    get_user_groups,
    get_all_permissions,
    get_group_permissions,
    check_model_permission
)

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_permissions(request):
    """
    Endpoint para obtener todos los permisos del usuario autenticado.
    
    Returns:
        Response con permisos y grupos del usuario
    """
    try:
        user_perms = get_user_permissions(request.user)
        user_groups = get_user_groups(request.user)
        
        return Response({
            'permissions': user_perms,
            'groups': user_groups,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error al obtener permisos: {str(e)}")
        return Response(
            {'error': 'Error al obtener permisos del usuario'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_permission(request):
    """
    Endpoint para verificar un permiso específico.
    
    Query params:
        - model: Nombre del modelo
        - action: Acción a verificar (view, add, change, delete)
        
    Returns:
        Response indicando si tiene el permiso
    """
    model = request.GET.get('model')
    action = request.GET.get('action')
    
    if not model or not action:
        return Response(
            {'error': 'Se requieren los parámetros model y action'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        has_permission = check_model_permission(request.user, model, action)
        return Response({'has_permission': has_permission})
        
    except Exception as e:
        logger.error(f"Error al verificar permiso: {str(e)}")
        return Response(
            {'error': 'Error al verificar el permiso'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_permissions(request):
    """
    Endpoint para obtener todos los permisos disponibles.
    Solo accesible para usuarios staff.
    
    Returns:
        Response con todos los permisos agrupados por modelo
    """
    if not request.user.is_staff:
        return Response(
            {'error': 'Acceso no autorizado'},
            status=status.HTTP_403_FORBIDDEN
        )
        
    try:
        permissions = get_all_permissions()
        return Response(permissions, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error al obtener permisos disponibles: {str(e)}")
        return Response(
            {'error': 'Error al obtener permisos disponibles'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_perms(request, group_name):
    """
    Endpoint para obtener los permisos de un grupo específico.
    Solo accesible para usuarios staff.
    
    Args:
        group_name: Nombre del grupo
        
    Returns:
        Response con los permisos del grupo
    """
    if not request.user.is_staff:
        return Response(
            {'error': 'Acceso no autorizado'},
            status=status.HTTP_403_FORBIDDEN
        )
        
    try:
        permissions = get_group_permissions(group_name)
        return Response(permissions, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error al obtener permisos del grupo: {str(e)}")
        return Response(
            {'error': f'Error al obtener permisos del grupo {group_name}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
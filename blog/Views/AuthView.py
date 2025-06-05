"""
API Views para autenticación y gestión de perfiles de usuario.

Este módulo proporciona endpoints adicionales para la gestión
de usuarios y perfiles complementando rest_auth.
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)


def get_user_permissions(user):
    """
    Obtiene los permisos específicos del usuario para el frontend.
    Construye un diccionario que el frontend puede consumir fácilmente.
    """
    if not user.is_staff:
        return {}

    if user.is_superuser:
        all_perms = {'view': True, 'add': True, 'change': True, 'delete': True}
        return {
            'conferencias': all_perms.copy(), 'cursos': all_perms.copy(),
            'noticias': all_perms.copy(), 'integrantes': all_perms.copy(),
            'proyectos': all_perms.copy(), 'ofertas': all_perms.copy(),
            'auditlog': {'view': True, 'add': False, 'change': False, 'delete': True},
            'users': all_perms.copy(), 'groups': all_perms.copy(),
        }
    
    perms = {}
    models_to_check = {
        'conferencias': 'conferencia', 'cursos': 'cursos', 'noticias': 'noticia',
        'integrantes': 'integrantes', 'proyectos': 'proyectos', 'ofertas': 'ofertasempleo',
        'auditlog': 'auditlog'
    }
    auth_models = {'users': 'user', 'groups': 'group'}

    for frontend_name, model_name in models_to_check.items():
        perms[frontend_name] = {
            'view': user.has_perm(f'blog.view_{model_name}'),
            'add': user.has_perm(f'blog.add_{model_name}'),
            'change': user.has_perm(f'blog.change_{model_name}'),
            'delete': user.has_perm(f'blog.delete_{model_name}'),
        }

    for frontend_name, model_name in auth_models.items():
        perms[frontend_name] = {
            'view': user.has_perm(f'auth.view_{model_name}'),
            'add': user.has_perm(f'auth.add_{model_name}'),
            'change': user.has_perm(f'auth.change_{model_name}'),
            'delete': user.has_perm(f'auth.delete_{model_name}'),
        }
        
    return perms


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    Endpoint para obtener el perfil del usuario autenticado, incluyendo permisos.
    """
    try:
        user = request.user
        token, _ = Token.objects.get_or_create(user=user)
        
        profile_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'is_active': user.is_active,
            'token': token.key if token else None,
            'permissions': get_user_permissions(user)
        }
        
        logger.info(f"Perfil y permisos solicitados por usuario: {user.username}")
        return Response(profile_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error al obtener perfil de usuario: {e}", exc_info=True)
        return Response(
            {'error': 'Error interno al obtener el perfil del usuario'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """
    Endpoint para actualizar el perfil del usuario autenticado.
    
    Returns:
        Response: Perfil actualizado del usuario
    """
    try:
        user = request.user
        data = request.data
        
        # Campos que se pueden actualizar
        updatable_fields = ['first_name', 'last_name', 'email']
        
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        user.save()
        
        profile_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'is_active': user.is_active,
        }
        
        logger.info(f"Perfil actualizado por usuario: {user.username}")
        return Response(profile_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error al actualizar perfil de usuario: {str(e)}")
        return Response(
            {'error': 'Error al actualizar el perfil del usuario'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_auth_status(request):
    """
    Endpoint para verificar el estado de autenticación.
    
    Returns:
        Response: Estado de autenticación del usuario
    """
    try:
        if request.user.is_authenticated:
            user = request.user
            return Response({
                'authenticated': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'permissions': get_user_permissions(user),
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'authenticated': False,
                'user': None
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        logger.error(f"Error al verificar estado de autenticación: {str(e)}")
        return Response(
            {'error': 'Error al verificar el estado de autenticación'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

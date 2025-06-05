"""
API Views para autenticación y gestión de perfiles de usuario.

Este módulo proporciona endpoints adicionales para la gestión
de usuarios y perfiles complementando rest_auth.
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.contenttypes.models import ContentType
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """
    Endpoint para obtener el perfil del usuario autenticado.
    
    Returns:
        Response: Información del perfil del usuario
    """
    try:
        user = request.user
        
        # Obtener o crear token para el usuario
        token, created = Token.objects.get_or_create(user=user)
        
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
            'token': token.key if token else None
        }
        
        logger.info(f"Perfil solicitado por usuario: {user.username}")
        return Response(profile_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error al obtener perfil de usuario: {str(e)}")
        return Response(
            {'error': 'Error al obtener el perfil del usuario'}, 
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
            return Response({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'is_staff': request.user.is_staff,
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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_permissions(request):
    """
    Endpoint para obtener los permisos del usuario autenticado.
    
    Returns:
        Response: Lista de permisos del usuario por modelo
    """
    try:
        user = request.user
        
        # Obtener todos los permisos del usuario
        all_perms = []
        
        # Permisos directos del usuario
        for perm in user.user_permissions.all():
            all_perms.append({
                'model': perm.content_type.model,
                'codename': perm.codename,
                'name': perm.name
            })
            
        # Permisos a través de grupos
        for group in user.groups.all():
            for perm in group.permissions.all():
                all_perms.append({
                    'model': perm.content_type.model,
                    'codename': perm.codename,
                    'name': perm.name,
                    'group': group.name
                })
                
        # Organizar permisos por modelo
        perms_by_model = {}
        for perm in all_perms:
            model = perm['model']
            if model not in perms_by_model:
                perms_by_model[model] = []
            perms_by_model[model].append(perm)
            
        response_data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'groups': list(user.groups.values_list('name', flat=True))
            },
            'permissions': perms_by_model
        }
        
        logger.info(f"Permisos obtenidos para usuario: {user.username}")
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error al obtener permisos de usuario: {str(e)}")
        return Response(
            {'error': 'Error al obtener los permisos del usuario'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

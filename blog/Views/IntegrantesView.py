"""
API Views para gestión de integrantes.

Este módulo proporciona endpoints REST para gestionar integrantes
con capacidades avanzadas de filtrado y búsqueda.
"""

from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
import logging

from blog.Models.IntegrantesModel import Integrantes
from blog.Serializers.IntegrantesSerializer import IntegrantesSerializer
from blog.pagination import StandardResultsSetPagination
from blog.filters import IntegrantesFilter
from blog.Views.BaseModelViewSet import BaseModelViewSet

logger = logging.getLogger(__name__)

class IntegrantesViewSet(BaseModelViewSet):
    """
    ViewSet para gestionar integrantes.
    
    Proporciona operaciones CRUD completas para integrantes con:
    - Filtrado avanzado por nombre, rol y estado
    - Búsqueda en texto completo
    - Ordenamiento por múltiples campos
    - Rate limiting por usuario
    - Paginación automática
    
    **Filtros disponibles:**
    - `nombre`: Buscar por nombre del integrante
    - `rol`: Filtrar por rol
    - `estado`: Filtrar por estado (activo/inactivo)
    
    **Búsqueda:**
    Usar el parámetro `search` para buscar en nombre, rol y descripción.
    
    **Ordenamiento:**
    Usar `ordering` con campos: nombre, rol, fecha_ingreso
    """
    
    serializer_class = IntegrantesSerializer
    queryset = Integrantes.objects.all()
    pagination_class = StandardResultsSetPagination
    filterset_class = IntegrantesFilter
    search_fields = ['nombre_integrante', 'rol_integrante', 'descripcion_integrante']
    ordering_fields = ['nombre_integrante', 'rol_integrante', 'fecha_ingreso']
    ordering = ['nombre_integrante']  # Ordenamiento por defecto
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """
        Endpoint para obtener solo integrantes activos.
        
        Returns:
            Response: Lista de integrantes activos
        """
        self.check_action_permission(request, 'view')
        
        queryset = self.filter_queryset(
            self.get_queryset().filter(estado=True)
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
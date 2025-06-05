"""
API Views para gestión de conferencias.

Este módulo proporciona endpoints REST para gestionar conferencias
con capacidades avanzadas de filtrado y búsqueda.
"""

from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
import logging
from django.utils import timezone

from blog.Models.ConferenciasModel import Conferencias
from blog.Serializers.ConferenciasSerializer import ConferenciasSerializer
from blog.pagination import StandardResultsSetPagination
from blog.filters import ConferenciasFilter
from blog.Views.BaseModelViewSet import BaseModelViewSet

logger = logging.getLogger(__name__)

class ConferenciasViewSet(BaseModelViewSet):
    """
    ViewSet para gestionar conferencias.
    
    Proporciona operaciones CRUD completas para conferencias con:
    - Filtrado avanzado por nombre, ponente y fechas
    - Búsqueda en texto completo
    - Ordenamiento por múltiples campos
    - Rate limiting por usuario
    - Paginación automática
    
    **Filtros disponibles:**
    - `nombre`: Buscar por nombre de conferencia
    - `ponente`: Buscar por nombre del ponente
    - `fecha_desde`: Conferencias desde una fecha específica
    - `fecha_hasta`: Conferencias hasta una fecha específica
    - `proximas`: Solo conferencias futuras (true/false)
    
    **Búsqueda:**
    Usar el parámetro `search` para buscar en nombre, ponente y descripción.
    
    **Ordenamiento:**
    Usar `ordering` con campos: fecha_conferencia, nombre_conferencia, ponente_conferencia
    """
    
    serializer_class = ConferenciasSerializer
    queryset = Conferencias.objects.all()
    pagination_class = StandardResultsSetPagination
    filterset_class = ConferenciasFilter
    search_fields = ['nombre_conferencia', 'ponente_conferencia', 'descripcion_conferencia']
    ordering_fields = ['fecha_conferencia', 'nombre_conferencia', 'ponente_conferencia']
    ordering = ['-fecha_conferencia']  # Ordenamiento por defecto
    
    @action(detail=False, methods=['get'])
    def proximas(self, request):
        """
        Endpoint para obtener solo conferencias futuras.
        
        Returns:
            Response: Lista de conferencias futuras
        """
        self.check_action_permission(request, 'view')
        
        queryset = self.filter_queryset(
            self.get_queryset().filter(fecha_conferencia__gte=timezone.now())
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
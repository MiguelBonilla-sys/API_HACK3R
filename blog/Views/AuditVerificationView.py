"""
Vista específica para verificación de auditoría desde el frontend.
Proporciona endpoints simples para verificar que los triggers funcionan.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from typing import Optional, Dict, Any, List

from blog.Models.AuditLogModel import AuditLog
from blog.Serializers.AuditLogSerializer import AuditLogSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def audit_verification_status(request) -> Response:
    """
    Endpoint para verificar el estado de la auditoría.
    
    Returns:
        Response: Estado completo del sistema de auditoría
    """
    
    # Estadísticas básicas
    total_logs = AuditLog.objects.count()
    
    # Logs de las últimas 24 horas
    hace_24h = timezone.now() - timedelta(hours=24)
    logs_24h = AuditLog.objects.filter(timestamp__gte=hace_24h).count()
    
    # Logs por tabla
    logs_por_tabla = (AuditLog.objects
                     .values('table_name')
                     .annotate(count=Count('id'))
                     .order_by('-count'))
    
    # Logs por tipo de operación
    logs_por_tipo = (AuditLog.objects
                    .values('change_type')
                    .annotate(count=Count('id'))
                    .order_by('-count'))
    
    # Últimos 5 logs
    recent_logs = AuditLog.objects.order_by('-timestamp')[:5]
    recent_logs_data = AuditLogSerializer(recent_logs, many=True).data
    
    # Estado de los triggers (verificar si hay actividad reciente)
    expected_tables = [
        'blog_conferencias',
        'blog_integrantes', 
        'blog_noticias',
        'blog_cursos',
        'blog_ofertasempleo',
        'blog_proyectos'
    ]
    
    tables_with_logs = set(item['table_name'] for item in logs_por_tabla)
    coverage: float = len(tables_with_logs & set(expected_tables)) / len(expected_tables) * 100
    
    data: Dict[str, Any] = {
        'status': 'operational' if total_logs > 0 else 'inactive',
        'total_logs': total_logs,
        'logs_24_horas': logs_24h,
        'cobertura_tablas': f"{coverage:.1f}%",
        'tablas_auditadas': list(tables_with_logs),
        'logs_por_tabla': list(logs_por_tabla),
        'logs_por_tipo': list(logs_por_tipo),
        'ultimos_logs': recent_logs_data,
        'timestamp_verificacion': timezone.now()
    }
    
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def audit_logs_simple(request) -> Response:
    """
    Endpoint simplificado para obtener logs de auditoría.
    
    Query params:
        - limit: número de logs a retornar (default: 20)
        - table: filtrar por tabla específica
        - type: filtrar por tipo de operación
    """
    
    try:
        limit: int = int(request.GET.get('limit', 20))
    except (ValueError, TypeError):
        limit = 20
    
    table_filter: Optional[str] = request.GET.get('table')
    type_filter: Optional[str] = request.GET.get('type')
    
    queryset = AuditLog.objects.all()
    
    if table_filter:
        queryset = queryset.filter(table_name=table_filter)
    
    if type_filter:
        queryset = queryset.filter(change_type=type_filter)
    
    logs = queryset.order_by('-timestamp')[:limit]
    
    # Formato simplificado para el frontend
    logs_data: List[Dict[str, Any]] = []
    for log in logs:
        logs_data.append({
            'id': log.pk,  # Usar pk en lugar de id para mayor claridad
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'usuario': log.user.username if log.user else 'Usuario eliminado',
            'tabla': log.table_name.replace('blog_', ''),  # Simplificar nombre
            'accion': log.change_type,
            'record_id': log.affected_record_id,
            'datos': log.modified_data
        })
    
    return Response({
        'logs': logs_data,
        'total': queryset.count(),
        'limit': limit
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_audit_trigger(request) -> Response:
    """
    Endpoint para probar triggers desde el frontend.
    Crea una conferencia de prueba y verifica que se registre.
    """
    
    from blog.Models.ConferenciasModel import Conferencias
    
    # Contar logs antes
    logs_before = AuditLog.objects.count()
    
    try:
        # Crear conferencia de prueba
        conferencia = Conferencias.objects.create(
            nombre_conferencia=f"Test Frontend {timezone.now().strftime('%H:%M:%S')}",
            ponente_conferencia="Frontend Tester",
            descripcion_conferencia="Verificación desde el frontend",
            imagen_conferencia="https://test.com/frontend.jpg",
            link_conferencia="https://frontend.test.com",
            creador=request.user
        )
        
        # Verificar si se creó log
        logs_after = AuditLog.objects.count()
        
        if logs_after > logs_before:
            # Obtener el log creado
            new_log: Optional[AuditLog] = AuditLog.objects.order_by('-timestamp').first()
            
            # Limpiar - eliminar la conferencia de prueba
            conferencia.delete()
            
            logs_final = AuditLog.objects.count()
            
            # Verificar que el log existe antes de acceder a sus atributos
            if new_log is not None:
                return Response({
                    'status': 'success',
                    'message': 'Trigger funcionando correctamente',
                    'logs_before': logs_before,
                    'logs_after': logs_after,
                    'logs_final': logs_final,
                    'created_log': {
                        'id': new_log.pk,  # Usar pk en lugar de id
                        'timestamp': new_log.timestamp.isoformat(),
                        'table': new_log.table_name,
                        'action': new_log.change_type,
                        'user': new_log.user.username if new_log.user else 'Usuario eliminado'
                    },
                    'triggers_tested': ['CREATE', 'DELETE']
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Log creado pero no se pudo recuperar',
                    'logs_before': logs_before,
                    'logs_after': logs_after,
                    'logs_final': logs_final
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Limpiar en caso de fallo
            conferencia.delete()
            
            return Response({
                'status': 'error',
                'message': 'Trigger no está funcionando',
                'logs_before': logs_before,
                'logs_after': logs_after
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Error al probar trigger: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
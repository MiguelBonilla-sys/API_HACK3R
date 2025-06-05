#!/usr/bin/env python
"""
Script maestro para verificación completa del sistema de auditoría.

Este script guía al usuario a través de todos los pasos necesarios
para verificar que el sistema de auditoría funciona correctamente.
"""

import os
import django
import time
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.Models.AuditLogModel import AuditLog
from django.db import connection
from django.contrib.auth.models import User

def print_header(title):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def print_step(step, description):
    """Imprime un paso de verificación."""
    print(f"\n📋 PASO {step}: {description}")
    print("-" * 50)

def check_triggers_status():
    """Verifica el estado de todos los triggers."""
    print_header("VERIFICACIÓN DE TRIGGERS")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                event_object_table,
                COUNT(*) as trigger_count
            FROM information_schema.triggers 
            WHERE trigger_schema = 'public' 
                AND trigger_name LIKE 'trigger_log_%'
            GROUP BY event_object_table
            ORDER BY event_object_table;
        """)
        
        results = cursor.fetchall()
    
    expected_tables = [
        'blog_conferencias',
        'blog_integrantes', 
        'blog_noticias',
        'blog_cursos',
        'blog_ofertasempleo',
        'blog_proyectos'
    ]
    
    found_tables = {table: count for table, count in results}
    total_triggers = sum(found_tables.values())
    
    print(f"📊 ESTADO DE TRIGGERS: {total_triggers}/18")
    
    for table in expected_tables:
        if table in found_tables:
            count = found_tables[table]
            status = "✅ COMPLETO" if count == 3 else f"⚠️  PARCIAL ({count}/3)"
            print(f"   🏷️  {table}: {status}")
        else:
            print(f"   🏷️  {table}: ❌ SIN TRIGGERS")
    
    coverage = (total_triggers / 18) * 100
    print(f"\n📈 COBERTURA TOTAL: {coverage:.1f}%")
    
    return total_triggers >= 18

def check_audit_logs():
    """Verifica el estado de los logs de auditoría."""
    print_header("VERIFICACIÓN DE LOGS DE AUDITORÍA")
    
    total_logs = AuditLog.objects.count()
    print(f"📊 Total de registros: {total_logs}")
    
    if total_logs > 0:
        # Mostrar últimos logs
        recent = AuditLog.objects.order_by('-timestamp')[:5]
        print(f"\n📋 ÚLTIMOS 5 REGISTROS:")
        for i, log in enumerate(recent, 1):
            print(f"   {i}. {log.timestamp.strftime('%H:%M:%S')} - {log.change_type} en {log.table_name} por {log.user.username}")
        
        # Estadísticas por tabla
        from django.db.models import Count
        by_table = AuditLog.objects.values('table_name').annotate(count=Count('id')).order_by('-count')
        
        print(f"\n🏷️ REGISTROS POR TABLA:")
        for item in by_table:
            print(f"   - {item['table_name']}: {item['count']} registros")
    else:
        print("⚠️  No hay registros de auditoría aún")
    
    return total_logs

def interactive_verification():
    """Guía interactiva para verificación manual."""
    print_header("VERIFICACIÓN INTERACTIVA")
    
    print("🎯 Ahora vamos a hacer una verificación manual paso a paso")
    print("📋 Sigue las instrucciones para confirmar que todo funciona")
    
    input("\n🚀 Presiona ENTER para continuar...")
    
    print_step(1, "Verificación desde Django Admin")
    print("🌐 Abre tu navegador y ve a:")
    print("   URL: http://localhost:8000/admin/blog/auditlog/")
    print("   (o tu dominio si está en Railway)")
    print("\n📋 Debes ver:")
    print("   - Lista de logs de auditoría")
    print("   - Filtros por usuario, tabla, tipo")
    print("   - Detalles JSON de cada operación")
    
    input("\n✅ Confirma que puedes ver los logs en Django Admin. Presiona ENTER...")
    
    print_step(2, "Verificación desde Frontend")
    print("🌐 Abre otra pestaña y ve a:")
    print("   URL: http://localhost:3000/admin/audit")
    print("   (o tu dominio del frontend)")
    print("\n📋 Debes ver:")
    print("   - Dashboard con estadísticas")
    print("   - Estado del sistema: 'Operativo'")
    print("   - Total de logs y cobertura")
    print("   - Botón 'Probar Triggers'")
    
    input("\n✅ Confirma que el dashboard se carga correctamente. Presiona ENTER...")
    
    print_step(3, "Test Automático desde Frontend")
    print("🧪 En el dashboard del frontend:")
    print("   1. Haz clic en 'Probar Triggers'")
    print("   2. Espera el resultado")
    print("   3. Debe mostrar '✅ Trigger funcionando correctamente'")
    
    input("\n✅ Confirma que el test automático funciona. Presiona ENTER...")
    
    print_step(4, "Verificación Manual - Conferencias")
    print("📝 Vamos a probar manualmente:")
    print("   1. Ve a http://localhost:3000/admin/conferencias")
    print("   2. Haz clic en 'Nueva Conferencia'")
    print("   3. Completa el formulario:")
    print("      - Nombre: 'Test de Auditoría Manual'")
    print("      - Ponente: 'Usuario Verificador'")
    print("      - Descripción: 'Verificación del sistema'")
    print("      - Link: 'https://test.com'")
    print("   4. Guarda la conferencia")
    
    input("\n✅ Conferencia creada. Presiona ENTER para verificar el log...")
    
    # Verificar si apareció nuevo log
    recent_log = AuditLog.objects.order_by('-timestamp').first()
    if recent_log and recent_log.table_name == 'blog_conferencias' and recent_log.change_type == 'CREATE':
        print("✅ ¡PERFECTO! Se detectó el nuevo log CREATE")
        print(f"   📝 Usuario: {recent_log.user.username}")
        print(f"   🕐 Tiempo: {recent_log.timestamp}")
    else:
        print("⚠️  No se detectó el log inmediatamente, puede tardar unos segundos")
    
    print("\n📝 Ahora edita esa conferencia:")
    print("   1. Cambia el nombre a 'Test de Auditoría Manual - EDITADO'")
    print("   2. Guarda los cambios")
    
    input("\n✅ Conferencia editada. Presiona ENTER para verificar...")
    
    print("\n📝 Finalmente elimina la conferencia:")
    print("   1. Ve a la lista de conferencias")
    print("   2. Elimina la conferencia de prueba")
    
    input("\n✅ Conferencia eliminada. Presiona ENTER para continuar...")

def final_summary():
    """Muestra el resumen final de la verificación."""
    print_header("RESUMEN FINAL DE VERIFICACIÓN")
    
    # Estado final
    total_logs = AuditLog.objects.count()
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.triggers 
            WHERE trigger_schema = 'public' 
                AND trigger_name LIKE 'trigger_log_%'
        """)
        trigger_count = cursor.fetchone()[0]
    
    print("🎯 ESTADO FINAL DEL SISTEMA:")
    print(f"   📊 Triggers instalados: {trigger_count}/18")
    print(f"   📈 Logs de auditoría: {total_logs}")
    print(f"   🕐 Última verificación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if trigger_count >= 18 and total_logs > 0:
        print("\n🎉 ¡FELICITACIONES!")
        print("✅ Tu sistema de auditoría está 100% funcional")
        print("📋 Todas las operaciones se registrarán automáticamente")
    else:
        print("\n⚠️  VERIFICACIÓN INCOMPLETA")
        print("🔧 Revisa la guía de resolución de problemas")
    
    print("\n📚 RECURSOS ADICIONALES:")
    print("   - Guía completa: GUIA_VERIFICACION_AUDITORIA.md")
    print("   - Monitor en tiempo real: python real_time_audit_verification.py monitor")
    print("   - Test rápido: python real_time_audit_verification.py test")
    
    print("\n🔗 ACCESO A LOS LOGS:")
    print("   - Django Admin: /admin/blog/auditlog/")
    print("   - Frontend Dashboard: /admin/audit")
    print("   - API: /api/audit/status/")

def main():
    """Función principal del script de verificación."""
    print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA DE AUDITORÍA")
    print("=" * 60)
    print("📋 Este script te guiará paso a paso para verificar")
    print("    que tu sistema de auditoría funciona correctamente")
    print("=" * 60)
    
    print("\n🚀 ¿Estás listo para comenzar?")
    print("   - Asegúrate de que Django esté corriendo")
    print("   - Asegúrate de que el frontend esté corriendo")
    print("   - Ten ambos navegadores listos")
    
    input("\n✅ Presiona ENTER para comenzar la verificación...")
    
    # Paso 1: Verificar triggers
    triggers_ok = check_triggers_status()
    
    if not triggers_ok:
        print("\n❌ ALTO: Los triggers no están completos")
        print("🔧 Ejecuta primero: python complete_missing_triggers.py")
        return
    
    # Paso 2: Verificar logs
    initial_logs = check_audit_logs()
    
    # Paso 3: Verificación interactiva
    interactive_verification()
    
    # Paso 4: Resumen final
    final_summary()
    
    print("\n" + "=" * 60)
    print("🎉 ¡VERIFICACIÓN COMPLETA TERMINADA!")
    print("📋 Tu sistema de auditoría está listo para usar")
    print("=" * 60)

if __name__ == "__main__":
    main() 
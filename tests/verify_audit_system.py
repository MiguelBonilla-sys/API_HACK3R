#!/usr/bin/env python
"""
Script para verificar y reparar el sistema de auditoría de Django.

Este script:
1. Verifica que los triggers estén configurados correctamente
2. Prueba el sistema de auditoría
3. Aplica correcciones si es necesario

Uso: python verify_audit_system.py
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection
from django.contrib.auth.models import User

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.Models.AuditLogModel import AuditLog
from blog.Models.ConferenciasModel import Conferencias
from blog.Models.IntegrantesModel import Integrantes
from blog.Models.NoticiasModel import Noticias
from blog.Models.CursosModel import Cursos


def check_database_triggers():
    """Verifica si los triggers están configurados en la base de datos."""
    print("🔍 Verificando triggers en la base de datos...")
    
    with connection.cursor() as cursor:
        # Consultar triggers existentes
        cursor.execute("""
            SELECT 
                trigger_name,
                event_object_table,
                action_timing,
                event_manipulation
            FROM information_schema.triggers 
            WHERE trigger_schema = 'public' 
                AND trigger_name LIKE 'trigger_log_%'
            ORDER BY event_object_table, trigger_name;
        """)
        
        triggers = cursor.fetchall()
        
        if triggers:
            print("✅ Triggers encontrados:")
            for trigger in triggers:
                print(f"   - {trigger[0]} en {trigger[1]} ({trigger[2]} {trigger[3]})")
        else:
            print("❌ No se encontraron triggers de auditoría")
            
        return len(triggers) > 0


def check_audit_table():
    """Verifica que la tabla de auditoría existe y está accesible."""
    print("\n📊 Verificando tabla de auditoría...")
    
    try:
        count = AuditLog.objects.count()
        print(f"✅ Tabla blog_auditlog accesible. Registros actuales: {count}")
        
        # Mostrar últimos 5 registros si existen
        if count > 0:
            print("📋 Últimos 5 registros de auditoría:")
            recent_logs = AuditLog.objects.order_by('-timestamp')[:5]
            for log in recent_logs:
                print(f"   - {log.timestamp}: {log.change_type} en {log.table_name} por {log.user.username}")
        
        return True
    except Exception as e:
        print(f"❌ Error accediendo a la tabla de auditoría: {e}")
        return False


def test_audit_functionality():
    """Prueba que el sistema de auditoría funcione correctamente."""
    print("\n🧪 Probando funcionalidad de auditoría...")
    
    try:
        # Obtener o crear un usuario de prueba
        user, created = User.objects.get_or_create(
            username='audit_test_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            print("👤 Usuario de prueba creado")
        
        # Contar registros antes
        initial_count = AuditLog.objects.count()
        print(f"📊 Registros de auditoría antes de la prueba: {initial_count}")
        
        # Crear una conferencia de prueba
        conferencia = Conferencias.objects.create(
            nombre_conferencia="Conferencia de Prueba Auditoría",
            ponente_conferencia="Ponente de Prueba",
            descripcion_conferencia="Esta es una conferencia de prueba para verificar el sistema de auditoría",
            imagen_conferencia="https://res.cloudinary.com/test/image/upload/test.jpg",
            link_conferencia="https://example.com/test",
            creador=user
        )
        
        print(f"✅ Conferencia de prueba creada con ID: {conferencia.idconferencia}")
        
        # Verificar si se creó registro de auditoría
        final_count = AuditLog.objects.count()
        print(f"📊 Registros de auditoría después de la prueba: {final_count}")
        
        if final_count > initial_count:
            print("✅ ¡Sistema de auditoría funcionando correctamente!")
            
            # Mostrar el registro creado
            new_log = AuditLog.objects.order_by('-timestamp').first()
            print(f"📝 Nuevo registro: {new_log.change_type} en {new_log.table_name}")
            print(f"   Datos: {new_log.modified_data}")
        else:
            print("❌ No se creó registro de auditoría. Los triggers no están funcionando.")
        
        # Probar actualización
        print("\n🔄 Probando actualización...")
        conferencia.nombre_conferencia = "Conferencia Actualizada"
        conferencia.save()
        
        update_count = AuditLog.objects.count()
        if update_count > final_count:
            print("✅ Trigger de UPDATE funcionando")
        else:
            print("❌ Trigger de UPDATE no funciona")
        
        # Limpiar - eliminar conferencia de prueba
        print("\n🗑️ Probando eliminación...")
        conferencia.delete()
        
        delete_count = AuditLog.objects.count()
        if delete_count > update_count:
            print("✅ Trigger de DELETE funcionando")
        else:
            print("❌ Trigger de DELETE no funciona")
        
        return final_count > initial_count
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False


def apply_trigger_fixes():
    """Aplica las correcciones a los triggers."""
    print("\n🔧 Aplicando correcciones a los triggers...")
    
    # Leer el script SQL de corrección
    sql_file = 'fix_audit_triggers.sql'
    
    if not os.path.exists(sql_file):
        print(f"❌ No se encontró el archivo {sql_file}")
        return False
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        with connection.cursor() as cursor:
            # Ejecutar el script SQL
            cursor.execute(sql_script)
        
        print("✅ Script SQL aplicado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando correcciones: {e}")
        return False


def show_table_info():
    """Muestra información sobre las tablas y sus nombres."""
    print("\n📋 Información de tablas Django:")
    
    models = [
        ('Conferencias', Conferencias),
        ('Integrantes', Integrantes),
        ('Noticias', Noticias),
        ('Cursos', Cursos),
        ('AuditLog', AuditLog)
    ]
    
    for name, model in models:
        table_name = model._meta.db_table
        print(f"   - {name}: {table_name}")


def main():
    """Función principal del script."""
    print("🔍 VERIFICACIÓN DEL SISTEMA DE AUDITORÍA")
    print("=" * 50)
    
    # Mostrar información de tablas
    show_table_info()
    
    # Verificar tabla de auditoría
    audit_table_ok = check_audit_table()
    
    if not audit_table_ok:
        print("\n❌ La tabla de auditoría no está disponible. Verifica la migración.")
        return
    
    # Verificar triggers
    triggers_exist = check_database_triggers()
    
    if not triggers_exist:
        print("\n⚠️  No se encontraron triggers. Aplicando correcciones...")
        if apply_trigger_fixes():
            print("✅ Correcciones aplicadas. Verificando nuevamente...")
            triggers_exist = check_database_triggers()
    
    # Probar funcionalidad
    if triggers_exist:
        audit_working = test_audit_functionality()
        
        if audit_working:
            print("\n🎉 ¡Sistema de auditoría completamente funcional!")
        else:
            print("\n❌ Los triggers existen pero no funcionan correctamente")
    else:
        print("\n❌ No se pudieron configurar los triggers")
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN:")
    print(f"   - Tabla de auditoría: {'✅' if audit_table_ok else '❌'}")
    print(f"   - Triggers configurados: {'✅' if triggers_exist else '❌'}")
    if triggers_exist:
        print(f"   - Funcionamiento: {'✅' if 'audit_working' in locals() and audit_working else '❌'}")


if __name__ == "__main__":
    main() 
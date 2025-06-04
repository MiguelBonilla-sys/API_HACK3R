import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.Models.AuditLogModel import AuditLog
from blog.Models.ConferenciasModel import Conferencias

def test_audit_system():
    """Prueba el sistema de auditoría creando, actualizando y eliminando una conferencia."""
    
    print("🧪 PROBANDO SISTEMA DE AUDITORÍA")
    print("=" * 50)
    
    # Contar registros antes
    initial_count = AuditLog.objects.count()
    print(f"📊 Registros de auditoría iniciales: {initial_count}")
    
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
    else:
        print("👤 Usando usuario de prueba existente")
    
    print("\n🔄 Paso 1: Creando conferencia...")
    try:
        # Crear una conferencia de prueba
        conferencia = Conferencias.objects.create(
            nombre_conferencia="Conferencia de Prueba Auditoría",
            ponente_conferencia="Dr. Audit Test",
            descripcion_conferencia="Esta es una conferencia de prueba para verificar el sistema de auditoría",
            imagen_conferencia="https://res.cloudinary.com/test/image/upload/test.jpg",
            link_conferencia="https://example.com/test-conference",
            creador=user
        )
        
        print(f"✅ Conferencia creada con ID: {conferencia.idconferencia}")
        
        # Verificar si se creó registro de auditoría
        after_create_count = AuditLog.objects.count()
        print(f"📊 Registros después de crear: {after_create_count}")
        
        if after_create_count > initial_count:
            print("✅ ¡Trigger CREATE funcionando!")
            # Mostrar el registro creado
            new_log = AuditLog.objects.order_by('-timestamp').first()
            print(f"📝 Registro: {new_log.change_type} en {new_log.table_name}")
            print(f"   Usuario: {new_log.user.username}")
            print(f"   Datos: {new_log.modified_data}")
        else:
            print("❌ Trigger CREATE no funcionó")
            return False
            
    except Exception as e:
        print(f"❌ Error creando conferencia: {e}")
        return False
    
    print("\n🔄 Paso 2: Actualizando conferencia...")
    try:
        # Actualizar la conferencia
        conferencia.nombre_conferencia = "Conferencia Actualizada - Sistema de Auditoría"
        conferencia.ponente_conferencia = "Dr. Updated Auditor"
        conferencia.save()
        
        after_update_count = AuditLog.objects.count()
        print(f"📊 Registros después de actualizar: {after_update_count}")
        
        if after_update_count > after_create_count:
            print("✅ ¡Trigger UPDATE funcionando!")
            # Mostrar el registro de actualización
            update_log = AuditLog.objects.order_by('-timestamp').first()
            print(f"📝 Registro: {update_log.change_type} en {update_log.table_name}")
            print(f"   Datos: {update_log.modified_data}")
        else:
            print("❌ Trigger UPDATE no funcionó")
            
    except Exception as e:
        print(f"❌ Error actualizando conferencia: {e}")
    
    print("\n🔄 Paso 3: Eliminando conferencia...")
    try:
        # Eliminar la conferencia
        conferencia_id = conferencia.idconferencia
        conferencia.delete()
        
        after_delete_count = AuditLog.objects.count()
        print(f"📊 Registros después de eliminar: {after_delete_count}")
        
        if after_delete_count > after_update_count:
            print("✅ ¡Trigger DELETE funcionando!")
            # Mostrar el registro de eliminación
            delete_log = AuditLog.objects.order_by('-timestamp').first()
            print(f"📝 Registro: {delete_log.change_type} en {delete_log.table_name}")
            print(f"   Datos: {delete_log.modified_data}")
        else:
            print("❌ Trigger DELETE no funcionó")
            
    except Exception as e:
        print(f"❌ Error eliminando conferencia: {e}")
    
    # Resumen final
    final_count = AuditLog.objects.count()
    new_records = final_count - initial_count
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBA:")
    print(f"   - Registros iniciales: {initial_count}")
    print(f"   - Registros finales: {final_count}")
    print(f"   - Nuevos registros: {new_records}")
    
    if new_records >= 3:
        print("🎉 ¡Sistema de auditoría funcionando perfectamente!")
        print("📋 Últimos registros de auditoría:")
        recent_logs = AuditLog.objects.order_by('-timestamp')[:3]
        for i, log in enumerate(recent_logs, 1):
            print(f"   {i}. {log.timestamp.strftime('%H:%M:%S')} - {log.change_type} en {log.table_name}")
        return True
    else:
        print("⚠️  El sistema funciona parcialmente")
        return False

if __name__ == "__main__":
    test_audit_system() 
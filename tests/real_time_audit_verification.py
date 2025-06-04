import os
import django
import time
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.Models.AuditLogModel import AuditLog
from django.contrib.auth.models import User

class AuditVerifier:
    def __init__(self):
        self.last_check = datetime.now()
        self.initial_count = AuditLog.objects.count()
        
    def show_new_logs(self):
        """Muestra solo los logs nuevos desde la última verificación."""
        new_logs = AuditLog.objects.filter(
            timestamp__gt=self.last_check
        ).order_by('-timestamp')
        
        if new_logs.exists():
            print(f"\n🆕 {new_logs.count()} NUEVOS REGISTROS DE AUDITORÍA:")
            print("-" * 60)
            
            for log in new_logs:
                print(f"⏰ {log.timestamp.strftime('%H:%M:%S')}")
                print(f"👤 Usuario: {log.user.username}")
                print(f"🏷️  Tabla: {log.table_name}")
                print(f"🔄 Acción: {log.change_type}")
                print(f"🆔 Record ID: {log.affected_record_id}")
                print(f"📄 Datos: {log.modified_data}")
                print("-" * 40)
        else:
            print("⏳ Sin nuevos registros...")
        
        self.last_check = datetime.now()
        return new_logs.count()

    def show_summary(self):
        """Muestra un resumen del estado actual."""
        total = AuditLog.objects.count()
        new_since_start = total - self.initial_count
        
        print(f"\n📊 RESUMEN DE AUDITORÍA")
        print(f"📈 Registros totales: {total}")
        print(f"🆕 Nuevos desde inicio: {new_since_start}")
        
        # Últimos por tabla
        from django.db.models import Count
        by_table = AuditLog.objects.values('table_name').annotate(
            count=Count('id')
        ).order_by('-count')
        
        print(f"\n🏷️ REGISTROS POR TABLA:")
        for item in by_table:
            print(f"   {item['table_name']}: {item['count']}")

def monitor_audit_logs():
    """Monitor en tiempo real de los logs de auditoría."""
    verifier = AuditVerifier()
    
    print("🔍 MONITOR DE AUDITORÍA EN TIEMPO REAL")
    print("=" * 60)
    print("📋 Este script mostrará automáticamente los nuevos logs")
    print("🛑 Presiona Ctrl+C para detener")
    print("=" * 60)
    
    verifier.show_summary()
    
    try:
        while True:
            new_count = verifier.show_new_logs()
            
            if new_count > 0:
                print(f"✅ Detectados {new_count} nuevos registros!")
                verifier.show_summary()
            
            time.sleep(3)  # Verificar cada 3 segundos
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor detenido")
        verifier.show_summary()

def verify_backend_access():
    """Verifica el acceso a los logs desde el backend."""
    print("🔍 VERIFICACIÓN DE ACCESO AL BACKEND")
    print("=" * 50)
    
    # Verificar Django Admin
    print("1. 🌐 DJANGO ADMIN:")
    print("   📍 URL: http://localhost:8000/admin/blog/auditlog/")
    print("   📋 Aquí puedes ver todos los logs directamente")
    
    # Verificar API endpoints
    print("\n2. 🔌 API ENDPOINTS:")
    print("   📍 Todos los logs: /api/audit-logs/")
    print("   📍 Resumen: /api/audit-logs/resumen_actividad/")
    print("   📍 Errores: /api/audit-logs/errores_recientes/")
    
    # Mostrar estado actual
    total_logs = AuditLog.objects.count()
    print(f"\n3. 📊 ESTADO ACTUAL:")
    print(f"   📈 Total de logs: {total_logs}")
    
    if total_logs > 0:
        latest = AuditLog.objects.order_by('-timestamp').first()
        print(f"   🕐 Último registro: {latest.timestamp}")
        print(f"   👤 Usuario: {latest.user.username}")
        print(f"   🏷️  Tabla: {latest.table_name}")
        print(f"   🔄 Acción: {latest.change_type}")
    
    # Verificar usuarios
    users_count = User.objects.count()
    print(f"\n4. 👥 USUARIOS REGISTRADOS: {users_count}")
    recent_users = User.objects.order_by('-date_joined')[:3]
    for user in recent_users:
        print(f"   - {user.username} ({user.email})")

def create_test_operation():
    """Crea una operación de prueba para verificar los triggers."""
    from blog.Models.ConferenciasModel import Conferencias
    
    print("🧪 CREANDO OPERACIÓN DE PRUEBA")
    print("-" * 40)
    
    # Obtener usuario
    user, created = User.objects.get_or_create(
        username='backend_test',
        defaults={'email': 'backend@test.com'}
    )
    
    if created:
        print("👤 Usuario de prueba creado")
    
    # Contar antes
    before = AuditLog.objects.count()
    print(f"📊 Logs antes: {before}")
    
    # Crear conferencia
    conferencia = Conferencias.objects.create(
        nombre_conferencia="Test Backend Verification",
        ponente_conferencia="Backend Tester",
        descripcion_conferencia="Verificación desde el backend",
        imagen_conferencia="https://test.com/backend.jpg",
        link_conferencia="https://backend.test.com",
        creador=user
    )
    
    print(f"✅ Conferencia creada: {conferencia.nombre_conferencia}")
    
    # Verificar log
    after = AuditLog.objects.count()
    print(f"📊 Logs después: {after}")
    
    if after > before:
        print("✅ ¡Trigger funcionando! Log creado automáticamente")
        new_log = AuditLog.objects.order_by('-timestamp').first()
        print(f"📝 Registro: {new_log.change_type} en {new_log.table_name}")
    else:
        print("❌ No se detectó nuevo log")
    
    # Limpiar
    conferencia.delete()
    final = AuditLog.objects.count()
    
    if final > after:
        print("✅ Trigger DELETE también funcionando!")
    
    return after > before

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "monitor":
            monitor_audit_logs()
        elif command == "test":
            create_test_operation()
        elif command == "verify":
            verify_backend_access()
        else:
            print("Comandos disponibles: monitor, test, verify")
    else:
        print("🔍 VERIFICADOR DE AUDITORÍA BACKEND")
        print("=" * 40)
        print("Comandos disponibles:")
        print("  python real_time_audit_verification.py monitor  # Monitor en tiempo real")
        print("  python real_time_audit_verification.py test     # Crear operación de prueba")
        print("  python real_time_audit_verification.py verify   # Verificar acceso")
        print()
        verify_backend_access() 
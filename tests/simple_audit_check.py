import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection
from blog.Models.AuditLogModel import AuditLog

def check_triggers():
    """Verifica si los triggers están configurados en la base de datos."""
    print("Verificando triggers en la base de datos...")
    
    with connection.cursor() as cursor:
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
            print("Triggers encontrados:")
            for trigger in triggers:
                print(f"   - {trigger[0]} en {trigger[1]} ({trigger[2]} {trigger[3]})")
        else:
            print("No se encontraron triggers de auditoria")
            
        return len(triggers) > 0

def check_audit_count():
    """Verifica cuántos registros de auditoría hay."""
    count = AuditLog.objects.count()
    print(f"Registros de auditoria actuales: {count}")
    return count

if __name__ == "__main__":
    print("=== VERIFICACION RAPIDA DE AUDITORIA ===")
    check_triggers()
    check_audit_count() 
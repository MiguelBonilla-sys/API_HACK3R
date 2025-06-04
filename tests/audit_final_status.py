import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection
from blog.Models.AuditLogModel import AuditLog

def show_final_status():
    print("🎉 SISTEMA DE AUDITORÍA - ESTADO FINAL")
    print("=" * 60)
    
    # Verificar triggers
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
    
    # Organizar triggers por tabla
    tables = {}
    for trigger in triggers:
        table = trigger[1]
        if table not in tables:
            tables[table] = []
        tables[table].append(f"{trigger[2]} {trigger[3]}")
    
    print(f"📊 TRIGGERS INSTALADOS: {len(triggers)}/12")
    print("\n📋 ESTADO POR TABLA:")
    
    expected_tables = ['blog_conferencias', 'blog_integrantes', 'blog_noticias', 'blog_cursos']
    
    for table in expected_tables:
        if table in tables:
            triggers_count = len(tables[table])
            status = "✅ COMPLETO" if triggers_count == 3 else f"⚠️  PARCIAL ({triggers_count}/3)"
            print(f"\n   🏷️  {table}: {status}")
            for trigger_type in tables[table]:
                print(f"      - {trigger_type}")
        else:
            print(f"\n   🏷️  {table}: ❌ SIN TRIGGERS")
    
    # Mostrar registros de auditoría
    audit_count = AuditLog.objects.count()
    print(f"\n📊 REGISTROS DE AUDITORÍA: {audit_count}")
    
    if audit_count > 0:
        print("\n📋 ÚLTIMOS REGISTROS:")
        recent_logs = AuditLog.objects.order_by('-timestamp')[:5]
        for i, log in enumerate(recent_logs, 1):
            print(f"   {i}. {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {log.change_type} en {log.table_name} por {log.user.username}")
    
    # Análisis de cobertura
    coverage_percent = (len(triggers) / 12) * 100
    print(f"\n📊 COBERTURA DE AUDITORÍA: {coverage_percent:.1f}%")
    
    if coverage_percent >= 90:
        print("🎉 ¡SISTEMA PRÁCTICAMENTE COMPLETO!")
        print("✅ Tu sistema de auditoría está funcionando correctamente")
    elif coverage_percent >= 75:
        print("⚠️  SISTEMA MAYORMENTE FUNCIONAL")
        print("🔧 Algunos triggers faltantes, pero la funcionalidad principal está operativa")
    else:
        print("❌ SISTEMA INCOMPLETO")
        print("🔧 Necesita más configuración")
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES PARA USO:")
    print("1. 🖥️  Accede a tu frontend Next.js")
    print("2. ➕  Crea, edita o elimina conferencias, integrantes, noticias o cursos")
    print("3. 📊  Los cambios se registrarán automáticamente en blog_auditlog")
    print("4. 🔍  Revisa los logs desde el endpoint de auditoría en tu API")
    
    # Generar comando para ver los logs
    print(f"\n🔗 PARA VER LOS LOGS:")
    print("   - En Django Admin: /admin/blog/auditlog/")
    print("   - Via API: /api/audit-logs/")
    print("   - Resumen de actividad: /api/audit-logs/resumen_actividad/")

if __name__ == "__main__":
    show_final_status() 
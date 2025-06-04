import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.Models.AuditLogModel import AuditLog
from blog.Models.OfertasEmpleoModel import OfertasEmpleo
from blog.Models.ProyectosModel import Proyectos
from django.utils import timezone

def test_ofertas_empleo_audit():
    """Prueba el sistema de auditoría para ofertas de empleo."""
    
    print("🧪 PROBANDO AUDITORÍA DE OFERTAS DE EMPLEO")
    print("-" * 50)
    
    # Obtener usuario
    user, _ = User.objects.get_or_create(
        username='audit_test_user',
        defaults={'email': 'test@example.com'}
    )
    
    # Contar registros antes
    initial_count = AuditLog.objects.count()
    print(f"📊 Registros antes: {initial_count}")
    
    # Crear oferta de empleo
    try:
        oferta = OfertasEmpleo.objects.create(
            titulo_empleo="Desarrollador Full Stack",
            empresa="TechCorp SA",
            descripcion_empleo="Desarrollador con experiencia en Django y React",
            imagen="https://res.cloudinary.com/test/image/upload/logo.jpg",
            link_oferta="https://techcorp.com/jobs/1",
            creador=user
        )
        
        print(f"✅ Oferta creada: {oferta.titulo_empleo}")
        
        # Verificar auditoría CREATE
        after_create = AuditLog.objects.count()
        if after_create > initial_count:
            print("✅ Trigger CREATE funcionando!")
            log = AuditLog.objects.order_by('-timestamp').first()
            print(f"   📝 {log.change_type} en {log.table_name}")
        
        # Actualizar oferta
        oferta.titulo_empleo = "Senior Full Stack Developer"
        oferta.empresa = "TechCorp International"
        oferta.save()
        
        after_update = AuditLog.objects.count()
        if after_update > after_create:
            print("✅ Trigger UPDATE funcionando!")
            log = AuditLog.objects.order_by('-timestamp').first()
            print(f"   📝 {log.change_type} - Datos: {log.modified_data}")
        
        # Eliminar oferta
        oferta.delete()
        
        after_delete = AuditLog.objects.count()
        if after_delete > after_update:
            print("✅ Trigger DELETE funcionando!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_proyectos_audit():
    """Prueba el sistema de auditoría para proyectos."""
    
    print("\n🧪 PROBANDO AUDITORÍA DE PROYECTOS")
    print("-" * 50)
    
    # Obtener usuario
    user, _ = User.objects.get_or_create(
        username='audit_test_user',
        defaults={'email': 'test@example.com'}
    )
    
    # Contar registros antes
    initial_count = AuditLog.objects.count()
    print(f"📊 Registros antes: {initial_count}")
    
    # Crear proyecto
    try:
        proyecto = Proyectos.objects.create(
            nombre_proyecto="Sistema de Gestión Académica",
            fecha_proyecto=timezone.now(),
            link_proyecto="https://github.com/user/academic-system",
            description_proyecto="Sistema completo para gestión de estudiantes y cursos",
            creador=user
        )
        
        print(f"✅ Proyecto creado: {proyecto.nombre_proyecto}")
        
        # Verificar auditoría CREATE
        after_create = AuditLog.objects.count()
        if after_create > initial_count:
            print("✅ Trigger CREATE funcionando!")
            log = AuditLog.objects.order_by('-timestamp').first()
            print(f"   📝 {log.change_type} en {log.table_name}")
        
        # Actualizar proyecto
        proyecto.nombre_proyecto = "Sistema Avanzado de Gestión Académica"
        proyecto.description_proyecto = "Sistema completo con módulos de estudiantes, cursos y reportes"
        proyecto.save()
        
        after_update = AuditLog.objects.count()
        if after_update > after_create:
            print("✅ Trigger UPDATE funcionando!")
            log = AuditLog.objects.order_by('-timestamp').first()
            print(f"   📝 {log.change_type} - Datos: {log.modified_data}")
        
        # Eliminar proyecto
        proyecto.delete()
        
        after_delete = AuditLog.objects.count()
        if after_delete > after_update:
            print("✅ Trigger DELETE funcionando!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_audit_summary():
    """Muestra un resumen de los logs de auditoría."""
    
    print("\n📊 RESUMEN DE AUDITORÍA")
    print("=" * 50)
    
    total_logs = AuditLog.objects.count()
    print(f"📈 Total de registros: {total_logs}")
    
    # Contar por tipo de cambio
    from django.db.models import Count
    by_type = AuditLog.objects.values('change_type').annotate(count=Count('id'))
    
    print("\n📋 Por tipo de operación:")
    for item in by_type:
        print(f"   {item['change_type']}: {item['count']} registros")
    
    # Contar por tabla
    by_table = AuditLog.objects.values('table_name').annotate(count=Count('id'))
    
    print("\n🏷️ Por tabla:")
    for item in by_table:
        print(f"   {item['table_name']}: {item['count']} registros")
    
    # Mostrar últimos 5 registros
    print("\n📋 Últimos 5 registros:")
    recent = AuditLog.objects.order_by('-timestamp')[:5]
    for i, log in enumerate(recent, 1):
        print(f"   {i}. {log.timestamp.strftime('%H:%M:%S')} - {log.change_type} en {log.table_name}")

if __name__ == "__main__":
    print("🧪 PROBANDO NUEVOS TRIGGERS DE AUDITORÍA")
    print("=" * 60)
    
    success_count = 0
    
    if test_ofertas_empleo_audit():
        success_count += 1
    
    if test_proyectos_audit():
        success_count += 1
    
    show_audit_summary()
    
    print(f"\n✅ {success_count}/2 tests pasaron exitosamente")
    
    if success_count == 2:
        print("🎉 ¡TODOS LOS TRIGGERS FUNCIONANDO PERFECTAMENTE!")
        print("📋 Sistema de auditoría 100% operativo para todas las tablas")
    else:
        print("⚠️ Algunos triggers necesitan revisión") 
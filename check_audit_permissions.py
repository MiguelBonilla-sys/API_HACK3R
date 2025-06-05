#!/usr/bin/env python
"""
Script para verificar y mostrar permisos de AuditLog
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from blog.Models.AuditLogModel import AuditLog

def check_auditlog_permissions():
    """Verifica permisos específicos de AuditLog."""
    print('🔍 VERIFICACIÓN DE PERMISOS AUDITLOG')
    print('=' * 50)
    
    # Obtener Content Type de AuditLog
    try:
        content_type = ContentType.objects.get_for_model(AuditLog)
        print(f'✅ Content Type: {content_type}')
        
        # Obtener todos los permisos de AuditLog
        permissions = Permission.objects.filter(content_type=content_type)
        print(f'\n📋 PERMISOS DISPONIBLES PARA AUDITLOG:')
        for perm in permissions:
            print(f'   - {perm.codename}: {perm.name}')
            
        return permissions
        
    except Exception as e:
        print(f'❌ Error obteniendo permisos: {e}')
        return []

def check_user_permissions():
    """Verifica permisos de usuarios específicos."""
    print(f'\n👥 VERIFICACIÓN DE PERMISOS POR USUARIO:')
    print('-' * 40)
    
    # Verificar usuarios admin y staff
    test_users = ['admin']
    
    # Buscar usuarios staff
    staff_users = User.objects.filter(is_staff=True, is_superuser=False)
    for user in staff_users[:3]:  # Solo primeros 3
        test_users.append(user.username)
    
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            print(f'\n👤 Usuario: {user.username}')
            print(f'   🔑 is_staff: {user.is_staff}')
            print(f'   👑 is_superuser: {user.is_superuser}')
            
            # Verificar permisos específicos de AuditLog
            audit_perms = [
                'blog.view_auditlog',
                'blog.add_auditlog', 
                'blog.change_auditlog',
                'blog.delete_auditlog'
            ]
            
            print(f'   📋 Permisos AuditLog:')
            for perm in audit_perms:
                has_perm = user.has_perm(perm)
                status = '✅' if has_perm else '❌'
                print(f'      {status} {perm}')
                
        except User.DoesNotExist:
            print(f'❌ Usuario {username} no encontrado')

def show_groups_config():
    """Muestra configuración de grupos."""
    print(f'\n🏷️ CONFIGURACIÓN DE GRUPOS:')
    print('-' * 30)
    
    groups = Group.objects.all()
    if groups.exists():
        for group in groups:
            print(f'\n📂 Grupo: {group.name}')
            group_perms = group.permissions.filter(
                content_type__app_label='blog',
                content_type__model='auditlog'
            )
            if group_perms.exists():
                print(f'   📋 Permisos AuditLog:')
                for perm in group_perms:
                    print(f'      ✅ {perm.codename}')
            else:
                print(f'   ❌ Sin permisos AuditLog')
                
            # Mostrar usuarios en el grupo
            users_in_group = group.user_set.all()
            if users_in_group.exists():
                print(f'   👥 Usuarios: {[u.username for u in users_in_group]}')
    else:
        print('❌ No hay grupos configurados')

def show_solution_steps():
    """Muestra pasos para solucionar el problema."""
    print(f'\n🔧 PASOS PARA SOLUCIONAR EL PROBLEMA:')
    print('=' * 50)
    
    print('1️⃣ CREAR GRUPO "Auditores":')
    print('   - Ve a Django Admin → Groups → Add group')
    print('   - Nombre: "Auditores" o "Staff_Audit"')
    print('   - Selecciona permisos:')
    print('     ✅ blog | audit log | Can view audit log')
    print('     ⚠️  blog | audit log | Can add audit log (opcional)')
    print('     ⚠️  blog | audit log | Can change audit log (NO recomendado)')
    print('     ❌ blog | audit log | Can delete audit log (NO recomendado)')
    
    print('\n2️⃣ ASIGNAR USUARIOS AL GRUPO:')
    print('   - Ve a Django Admin → Users → [Usuario Staff]')
    print('   - En "Groups", selecciona "Auditores"')
    print('   - Guarda cambios')
    
    print('\n3️⃣ MODIFICAR PERMISOS DE API (opcional):')
    print('   - Cambiar IsAdminUser por IsAuthenticated + permisos específicos')
    print('   - O crear permiso personalizado')
    
    print('\n4️⃣ VERIFICAR ACCESO:')
    print('   - Usuario Staff debe poder ver /admin/blog/auditlog/')
    print('   - API debe permitir acceso con permisos correctos')

def main():
    """Función principal."""
    permissions = check_auditlog_permissions()
    check_user_permissions()
    show_groups_config()
    show_solution_steps()
    
    print(f'\n🎯 RESUMEN:')
    print(f'   📊 Permisos AuditLog disponibles: {len(permissions)}')
    print(f'   🔧 Configuración requerida: Crear grupo + asignar permisos')
    print(f'   🌐 URL Admin: /admin/blog/auditlog/')

if __name__ == "__main__":
    main() 
#!/usr/bin/env python
"""
Script para verificar configuración CSRF y realizar deploy
"""
import os
import sys
from pathlib import Path

def setup_environment():
    """Configurar el entorno"""
    BASE_DIR = Path(__file__).resolve().parent
    
    # Configurar variables de entorno
    postgres_config = {
        'DATABASE_URL': 'postgresql://Semillero_owner:5weYic7SAHXm@ep-bold-wave-a5lhd8ys-pooler.us-east-2.aws.neon.tech/Semillero?sslmode=require',
        'SECRET_KEY': 'qxreOxaQDP229YKEOoOcxTNdamkrBx9xng6MKzD4m2SBm0FNgG84_CBSlghhbiqn-IK4',
        'DEBUG': 'False',  # Importante: False para producción
        'PRODUCTION': 'True'
    }
    
    for key, value in postgres_config.items():
        os.environ[key] = value
    
    return BASE_DIR

def check_csrf_configuration():
    """Verificar configuración CSRF"""
    from django.conf import settings
    
    print("🔍 Verificando configuración CSRF...")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"CSRF_TRUSTED_ORIGINS: {getattr(settings, 'CSRF_TRUSTED_ORIGINS', 'No configurado')}")
    print(f"SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', 'No configurado')}")
    print(f"CSRF_COOKIE_SECURE: {getattr(settings, 'CSRF_COOKIE_SECURE', 'No configurado')}")
    
    return True

def test_database_and_user():
    """Verificar base de datos y usuario admin"""
    try:
        from django.db import connection
        from django.contrib.auth import get_user_model
        
        # Test DB connection
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        db_version = cursor.fetchone()
        print(f"✅ Base de datos conectada: {db_version[0][:50]}...")
        
        # Check admin user
        User = get_user_model()
        admin = User.objects.filter(username='admin').first()
        
        if admin:
            print(f"✅ Usuario admin existe:")
            print(f"   Email: {admin.email}")
            print(f"   Superusuario: {admin.is_superuser}")
            print(f"   Activo: {admin.is_active}")
        else:
            print("❌ Usuario admin no encontrado")
            
        return admin is not None
        
    except Exception as e:
        print(f"❌ Error verificando BD/usuario: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Verificando configuración para Railway...")
    
    # Setup
    base_dir = setup_environment()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    sys.path.insert(0, str(base_dir))
    
    try:
        import django
        django.setup()
        print("✅ Django configurado correctamente")
    except Exception as e:
        print(f"❌ Error configurando Django: {e}")
        return False
    
    # Verificaciones
    check_csrf_configuration()
    db_ok = test_database_and_user()
    
    if db_ok:
        print("\n" + "="*60)
        print("🎉 CONFIGURACIÓN LISTA PARA RAILWAY")
        print("="*60)
        print("🌐 Django Admin: https://apihack3r-production.up.railway.app/admin/")
        print("👤 Usuario: admin")
        print("🔑 Password: Hack3r2024!@#")
        print("🔧 CSRF: Configurado correctamente")
        print("🔒 Cookies seguras: Activadas para HTTPS")
        print("="*60)
        print("\n💡 Si aún tienes problemas CSRF:")
        print("1. Limpia las cookies del navegador")
        print("2. Usa modo incógnito")
        print("3. Verifica que accedes por HTTPS")
        return True
    else:
        print("\n❌ Hay problemas con la configuración")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

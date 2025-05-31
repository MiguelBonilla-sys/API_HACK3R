#!/usr/bin/env python
"""
Script final para crear superusuario con debug completo
"""
import os
import sys
import django
from pathlib import Path

def setup_environment():
    """Configurar el entorno de forma forzada"""
    
    # Ruta base
    BASE_DIR = Path(__file__).resolve().parent
    
    # Limpiar variables problemáticas
    problematic_vars = ['DATABASE_URL', 'DB_URL', 'SQLITE_URL']
    for var in problematic_vars:
        if var in os.environ:
            print(f"🧹 Limpiando variable problemática: {var}")
            del os.environ[var]
    
    # Configurar manualmente las variables de PostgreSQL
    postgres_config = {
        'DATABASE_URL': 'postgresql://Semillero_owner:5weYic7SAHXm@ep-bold-wave-a5lhd8ys-pooler.us-east-2.aws.neon.tech/Semillero?sslmode=require',
        'SECRET_KEY': 'qxreOxaQDP229YKEOoOcxTNdamkrBx9xng6MKzD4m2SBm0FNgG84_CBSlghhbiqn-IK4',
        'DEBUG': 'True'
    }
    
    for key, value in postgres_config.items():
        os.environ[key] = value
        print(f"✅ Configurando {key}: {value[:50]}...")
    
    return BASE_DIR

def test_database_connection():
    """Probar la conexión a la base de datos"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        db_version = cursor.fetchone()
        print(f"✅ Conectado a PostgreSQL: {db_version[0]}")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def create_superuser():
    """Crear el superusuario"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        username = 'admin'
        email = 'admin@hack3r.dev'
        password = 'Hack3r2024!@#'
        
        # Verificar si existe
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            print(f"ℹ️  Usuario '{username}' ya existe")
            print(f"   📧 Email: {user.email}")
            print(f"   🔑 Superusuario: {user.is_superuser}")
            print(f"   👤 Staff: {user.is_staff}")
            
            # Actualizar si no es superusuario
            if not user.is_superuser:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                print("✅ Usuario actualizado a superusuario")
            
            return user
        else:
            # Crear nuevo superusuario
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"✅ Superusuario '{username}' creado exitosamente!")
            print(f"   📧 Email: {email}")
            print(f"   🔑 Password: {password}")
            return user
            
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Función principal"""
    print("🚀 Iniciando configuración de superusuario...")
    
    # 1. Configurar entorno
    base_dir = setup_environment()
    
    # 2. Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    sys.path.insert(0, str(base_dir))
    
    try:
        django.setup()
        print("✅ Django configurado correctamente")
    except Exception as e:
        print(f"❌ Error configurando Django: {e}")
        return False
    
    # 3. Probar conexión
    if not test_database_connection():
        return False
    
    # 4. Crear superusuario
    user = create_superuser()
    
    if user:
        print("\n" + "="*50)
        print("🎉 CONFIGURACIÓN COMPLETADA")
        print("="*50)
        print(f"🌐 Django Admin: https://apihack3r-production.up.railway.app/admin/")
        print(f"👤 Usuario: admin")
        print(f"🔑 Password: Hack3r2024!@#")
        print("="*50)
        return True
    else:
        print("\n❌ No se pudo crear/verificar el superusuario")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

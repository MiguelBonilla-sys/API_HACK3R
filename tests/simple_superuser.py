#!/usr/bin/env python
"""
Script simple para verificar conexión DB y crear superusuario
"""
import os
import sys
from pathlib import Path

# Limpiar variables problemáticas
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

# Cargar .env
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'

# Leer y cargar manualmente las variables del .env
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

print(f"🔧 DATABASE_URL configurada: {os.getenv('DATABASE_URL', 'No encontrada')[:50]}...")

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.append(str(BASE_DIR))

try:
    import django
    django.setup()
    print("✅ Django configurado correctamente")
    
    # Verificar conexión a la base de datos
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    print("✅ Conexión a la base de datos exitosa")
    
    # Crear superusuario
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    username = 'admin'
    email = 'admin@hack3r.dev'
    password = 'Hack3r2024!@#'
    
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        print(f"ℹ️  Usuario '{username}' ya existe")
        print(f"   Email: {user.email}")
        print(f"   Superusuario: {user.is_superuser}")
    else:
        user = User.objects.create_superuser(username, email, password)
        print(f"✅ Superusuario '{username}' creado exitosamente!")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
    
    print(f"\n🌐 Accede al admin en: https://apihack3r-production.up.railway.app/admin/")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

#!/usr/bin/env python
"""
Script para limpiar variables de entorno y crear superusuario
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import django
from django.contrib.auth import get_user_model

# Limpiar variables problemáticas del entorno del sistema
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Cargar variables de entorno con prioridad al archivo .env
env_path = BASE_DIR / '.env'
load_dotenv(env_path, override=True)

# Verificar que tenemos las variables correctas
print(f"📁 Cargando .env desde: {env_path}")
print(f"📄 Archivo .env existe: {env_path.exists()}")
print(f"🔍 DATABASE_URL después de cargar .env: {os.getenv('DATABASE_URL', 'No encontrada')}")

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

User = get_user_model()

def create_superuser():
    """Crear superusuario si no existe"""
    
    # Datos del superusuario
    username = 'admin'
    email = 'admin@hack3r.dev'
    password = 'Hack3r2024!@#'  # Contraseña más segura
    
    print(f"\n🚀 Intentando crear superusuario...")
    print(f"👤 Username: {username}")
    print(f"📧 Email: {email}")
    
    # Verificar si ya existe
    if User.objects.filter(username=username).exists():
        print(f"❌ El usuario '{username}' ya existe.")
        user = User.objects.get(username=username)
        print(f"📧 Email actual: {user.email}")
        print(f"🔑 Es superusuario: {user.is_superuser}")
        print(f"👤 Es staff: {user.is_staff}")
        return user
    
    # Crear superusuario
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superusuario '{username}' creado exitosamente!")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"🚀 Puedes acceder al admin en: /admin/")
        print(f"🌐 URL completa: https://apihack3r-production.up.railway.app/admin/")
        return user
        
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")
        return None

if __name__ == '__main__':
    create_superuser()

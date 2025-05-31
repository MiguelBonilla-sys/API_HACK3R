#!/usr/bin/env python
"""
Script para verificar las variables de entorno
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo específico
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'
print(f"📁 Cargando .env desde: {env_path}")
print(f"📄 Archivo .env existe: {env_path.exists()}")
load_dotenv(env_path)

print("🔍 Verificando variables de entorno:")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY', 'No encontrada')}")
print(f"DEBUG: {os.getenv('DEBUG', 'No encontrada')}")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'No encontrada')}")
print(f"CLOUDINARY_CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME', 'No encontrada')}")
print(f"POSTGRES_USER: {os.getenv('POSTGRES_USER', 'No encontrada')}")
print(f"POSTGRES_PASSWORD: {os.getenv('POSTGRES_PASSWORD', 'No encontrada')}")

# Verificar todas las variables que empiecen con DATABASE o POSTGRES
print("\n🔍 Variables relacionadas con base de datos:")
for key, value in os.environ.items():
    if 'DATABASE' in key or 'POSTGRES' in key:
        print(f"{key}: {value[:50]}..." if len(value) > 50 else f"{key}: {value}")

# Verificar la URL de la base de datos
database_url = os.getenv('DATABASE_URL')
if database_url:
    print(f"\n✅ DATABASE_URL encontrada: {database_url[:50]}...")
else:
    print("\n❌ DATABASE_URL no encontrada")

# Verificar si Django puede cargar la configuración
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    import django
    django.setup()
    
    from django.conf import settings
    print(f"\n🔧 Django configurado correctamente")
    print(f"DEBUG en Django: {settings.DEBUG}")
    print(f"Base de datos configurada: {settings.DATABASES['default']['NAME']}")
    
except Exception as e:
    print(f"\n❌ Error configurando Django: {e}")

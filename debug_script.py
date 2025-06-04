#!/usr/bin/env python
"""
Script de depuración para identificar problemas de configuración.
Ejecutar con: python debug_script.py
"""

import os
import sys
import django
from pathlib import Path

# Configurar el entorno de Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Error configurando Django: {e}")
    sys.exit(1)

def check_environment():
    """Verificar variables de entorno críticas."""
    print("🔍 Verificando variables de entorno...")
    
    env_vars = {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'DEBUG': os.getenv('DEBUG'),
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'CLOUDINARY_CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'CLOUDINARY_API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'CLOUDINARY_API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    }
    
    missing_vars = []
    for var, value in env_vars.items():
        if value:
            print(f"✅ {var}: Configurada")
        else:
            print(f"❌ {var}: NO configurada")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Variables faltantes: {', '.join(missing_vars)}")
        print("📋 Revisa el archivo CONFIGURACION.md para más detalles")
    else:
        print("\n✅ Todas las variables de entorno están configuradas")

def check_database():
    """Verificar conexión a la base de datos."""
    print("\n🗄️  Verificando conexión a la base de datos...")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        return False

def check_cloudinary():
    """Verificar configuración de Cloudinary."""
    print("\n☁️  Verificando configuración de Cloudinary...")
    
    try:
        import cloudinary
        from django.conf import settings
        
        config = settings.CLOUDINARY_STORAGE
        if config.get('CLOUD_NAME') and config.get('API_KEY') and config.get('API_SECRET'):
            print("✅ Configuración de Cloudinary completa")
            return True
        else:
            print("❌ Configuración de Cloudinary incompleta")
            return False
    except Exception as e:
        print(f"❌ Error verificando Cloudinary: {e}")
        return False

def check_models():
    """Verificar que los modelos se puedan importar correctamente."""
    print("\n📊 Verificando modelos...")
    
    models_to_check = [
        ('blog.Models.NoticiasModel', 'Noticias'),
        ('blog.Models.IntegrantesModel', 'Integrantes'),
        ('blog.Models.OfertasEmpleoModel', 'OfertasEmpleo'),
        ('blog.Models.ConferenciasModel', 'Conferencias'),
        ('blog.Models.CursosModel', 'Cursos'),
        ('blog.Models.ProyectosModel', 'Proyectos'),
    ]
    
    all_good = True
    for module_path, model_name in models_to_check:
        try:
            module = __import__(module_path, fromlist=[model_name])
            model = getattr(module, model_name)
            print(f"✅ Modelo {model_name}: OK")
        except Exception as e:
            print(f"❌ Modelo {model_name}: Error - {e}")
            all_good = False
    
    return all_good

def check_serializers():
    """Verificar que los serializers se puedan importar correctamente."""
    print("\n🔄 Verificando serializers...")
    
    serializers_to_check = [
        ('blog.Serializers.NoticiasSerializer', 'NoticiasSerializer'),
        ('blog.Serializers.IntegrantesSerializer', 'IntegrantesSerializer'),
        ('blog.Serializers.OfertasSerializer', 'OfertasEmpleoSerializer'),
        ('blog.Serializers.ConferenciasSerializer', 'ConferenciasSerializer'),
        ('blog.Serializers.CursosSerializer', 'CursosSerializer'),
        ('blog.Serializers.ProyectosSerializer', 'ProyectosSerializer'),
    ]
    
    all_good = True
    for module_path, serializer_name in serializers_to_check:
        try:
            module = __import__(module_path, fromlist=[serializer_name])
            serializer = getattr(module, serializer_name)
            print(f"✅ Serializer {serializer_name}: OK")
        except Exception as e:
            print(f"❌ Serializer {serializer_name}: Error - {e}")
            all_good = False
    
    return all_good

def run_api_test():
    """Hacer una prueba básica de la API."""
    print("\n🌐 Verificando endpoints de API...")
    
    try:
        from django.test import Client
        client = Client()
        
        # Probar endpoint de documentación
        response = client.get('/api/docs/')
        if response.status_code in [200, 301, 302]:
            print("✅ Endpoint de documentación: OK")
        else:
            print(f"⚠️  Endpoint de documentación: Status {response.status_code}")
        
        # Probar endpoint de auth status
        response = client.post('/api/hl4/v1/auth-status/', {})
        print(f"ℹ️  Auth status endpoint: Status {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error probando API: {e}")

def main():
    """Función principal del script de depuración."""
    print("🔧 SCRIPT DE DEPURACIÓN - Django Backend")
    print("=" * 50)
    
    # Ejecutar todas las verificaciones
    check_environment()
    db_ok = check_database()
    cloudinary_ok = check_cloudinary()
    models_ok = check_models()
    serializers_ok = check_serializers()
    
    if db_ok:
        run_api_test()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN:")
    
    if all([db_ok, cloudinary_ok, models_ok, serializers_ok]):
        print("✅ Todas las verificaciones pasaron correctamente")
        print("🚀 El backend debería funcionar sin problemas")
    else:
        print("❌ Se encontraron problemas en la configuración")
        print("📖 Revisa los errores anteriores y el archivo CONFIGURACION.md")
        print("🔗 Asegúrate de que todas las variables de entorno estén configuradas")

if __name__ == "__main__":
    main() 
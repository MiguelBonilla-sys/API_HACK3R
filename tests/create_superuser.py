#!/usr/bin/env python
"""
Script para crear un superusuario de forma programática
"""
import os
import django
from django.contrib.auth import get_user_model

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
    
    # Verificar si ya existe
    if User.objects.filter(username=username).exists():
        print(f"❌ El usuario '{username}' ya existe.")
        user = User.objects.get(username=username)
        print(f"📧 Email: {user.email}")
        print(f"🔑 Es superusuario: {user.is_superuser}")
        print(f"👤 Es staff: {user.is_staff}")
        return
    
    # Crear superusuario
    try:        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superusuario '{username}' creado exitosamente!")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"🚀 Puedes acceder al admin en: /admin/")
        print(f"🌐 URL completa: https://apihack3r-production.up.railway.app/admin/")
        
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")

if __name__ == '__main__':
    create_superuser()

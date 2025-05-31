import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User

# Verificar usuarios existentes
print("=== USUARIOS EXISTENTES ===")
users = User.objects.all()
if users:
    for user in users:
        print(f"Usuario: {user.username}")
        print(f"Email: {user.email}")
        print(f"Es superuser: {user.is_superuser}")
        print(f"Es staff: {user.is_staff}")
        print("-" * 30)
else:
    print("No hay usuarios en la base de datos")

# Crear superusuario si no existe
username = 'admin'
if not User.objects.filter(username=username).exists():
    print(f"\n=== CREANDO SUPERUSUARIO ===")
    user = User.objects.create_superuser(
        username='admin',
        email='admin@hack3r.dev',
        password='admin123456'
    )
    print(f"✅ Superusuario creado!")
    print(f"Username: admin")
    print(f"Password: admin123456")
    print(f"Email: admin@hack3r.dev")
else:
    print(f"\n❌ El usuario '{username}' ya existe")

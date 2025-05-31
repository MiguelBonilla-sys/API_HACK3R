import os
os.environ['DATABASE_URL'] = 'postgresql://Semillero_owner:5weYic7SAHXm@ep-bold-wave-a5lhd8ys-pooler.us-east-2.aws.neon.tech/Semillero?sslmode=require'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print("=== ESTADO DE LA BASE DE DATOS ===")
print(f"Total usuarios: {User.objects.count()}")

for user in User.objects.all():
    print(f"- {user.username} ({user.email})")
    print(f"  Superusuario: {user.is_superuser}")
    print(f"  Staff: {user.is_staff}")
    print(f"  Activo: {user.is_active}")
    print()

# Intentar crear superusuario si no existe
admin_exists = User.objects.filter(username='admin').exists()
if not admin_exists:
    print("Creando superusuario...")
    try:
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@hack3r.dev',
            password='Hack3r2024!@#'
        )
        print("✅ Superusuario creado exitosamente!")
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("ℹ️ Usuario admin ya existe")

print("\n=== ACCESO AL ADMIN ===")
print("URL: https://apihack3r-production.up.railway.app/admin/")
print("Usuario: admin")
print("Password: Hack3r2024!@#")

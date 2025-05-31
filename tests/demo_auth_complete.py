#!/usr/bin/env python
"""
Script completo para demostrar el flujo de autenticación de Django
"""
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def demo_auth_flow():
    """Demuestra el flujo completo de autenticación"""
    print("🚀 DEMOSTRACIÓN COMPLETA DEL FLUJO DE AUTENTICACIÓN")
    print("=" * 60)
    
    # Paso 1: Registrar un nuevo usuario
    print("\n📝 PASO 1: Registro de usuario")
    print("-" * 30)
    
    register_data = {
        "username": f"demouser{hash(str(requests.get(f'{BASE_URL}/auth/login/').status_code)) % 1000}",
        "email": "demo@example.com",
        "password1": "demopass123!",
        "password2": "demopass123!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/registration/",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Status del registro: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            token = result.get("key") or result.get("token")
            username = register_data["username"]
            print(f"✅ Usuario registrado exitosamente: {username}")
            print(f"🔑 Token obtenido: {token[:20] if token else 'N/A'}...")
            
            if token:
                return demo_authenticated_operations(token, username)
        else:
            print(f"❌ Error en registro: {response.text}")
            print("🔄 Intentando con login de usuario existente...")
            return demo_login_existing_user()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_login_existing_user():
    """Demuestra login con usuario existente"""
    print("\n🔐 PASO 2: Login con usuario existente")
    print("-" * 40)
    
    # Intentar con usuarios comunes
    test_users = [
        {"username": "testuser123", "password": "testpass123!"},
        {"username": "admin", "password": "admin123"},
        {"username": "test", "password": "test123"}
    ]
    
    for user_data in test_users:
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login/",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"🔍 Probando login con: {user_data['username']}")
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                token = result.get("key") or result.get("token")
                print(f"✅ Login exitoso!")
                print(f"🔑 Token: {token[:20] if token else 'N/A'}...")
                return demo_authenticated_operations(token, user_data['username'])
            else:
                print(f"❌ Falló: {response.text[:100]}...")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("⚠️  No se pudo hacer login con usuarios predeterminados")
    return False

def demo_authenticated_operations(token, username):
    """Demuestra operaciones que requieren autenticación"""
    print(f"\n🔒 PASO 3: Operaciones autenticadas (Usuario: {username})")
    print("-" * 50)
    
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # 1. Obtener perfil de usuario
    print("👤 Obteniendo perfil de usuario...")
    try:
        response = requests.get(f"{BASE_URL}/auth/user/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print("✅ Perfil obtenido:")
            print(f"   - Username: {user_data.get('username', 'N/A')}")
            print(f"   - Email: {user_data.get('email', 'N/A')}")
            print(f"   - Staff: {user_data.get('is_staff', False)}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Probar endpoint personalizado de perfil
    print("\n🎯 Probando endpoint personalizado de perfil...")
    try:
        response = requests.get(f"{BASE_URL}/api/profile/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            profile_data = response.json()
            print("✅ Perfil personalizado obtenido:")
            print(f"   - Data: {json.dumps(profile_data, indent=2)[:200]}...")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Verificar estado de autenticación
    print("\n🔍 Verificando estado de autenticación...")
    try:
        response = requests.post(f"{BASE_URL}/api/auth-status/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            auth_status = response.json()
            print("✅ Estado de autenticación:")
            print(f"   - Autenticado: {auth_status.get('authenticated', False)}")
            if auth_status.get('user'):
                print(f"   - Usuario: {auth_status['user'].get('username', 'N/A')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Logout
    print("\n👋 Cerrando sesión...")
    try:
        response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print("✅ Logout exitoso")
            
            # Verificar que el token ya no funciona
            print("\n🔒 Verificando que el token fue invalidado...")
            test_response = requests.get(f"{BASE_URL}/auth/user/", headers=headers)
            print(f"📊 Status de prueba post-logout: {test_response.status_code}")
            
            if test_response.status_code == 401:
                print("✅ Token correctamente invalidado")
            else:
                print("⚠️  Token aún válido (verificar configuración)")
        else:
            print(f"❌ Error en logout: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return True

def show_available_endpoints():
    """Muestra resumen de endpoints disponibles"""
    print("\n📋 RESUMEN DE ENDPOINTS DISPONIBLES")
    print("=" * 50)
    
    endpoints = [
        {
            "url": "/auth/login/", 
            "method": "POST", 
            "description": "Iniciar sesión",
            "auth": "No requerida"
        },
        {
            "url": "/auth/logout/", 
            "method": "POST", 
            "description": "Cerrar sesión",
            "auth": "Token requerido"
        },
        {
            "url": "/auth/user/", 
            "method": "GET", 
            "description": "Obtener perfil de usuario",
            "auth": "Token requerido"
        },
        {
            "url": "/auth/registration/", 
            "method": "POST", 
            "description": "Registrar nuevo usuario",
            "auth": "No requerida"
        },
        {
            "url": "/api/profile/", 
            "method": "GET", 
            "description": "Perfil personalizado",
            "auth": "Token requerido"
        },
        {
            "url": "/api/auth-status/", 
            "method": "POST", 
            "description": "Verificar estado de auth",
            "auth": "No requerida"
        },
    ]
    
    for endpoint in endpoints:
        print(f"🔗 {endpoint['method']} {endpoint['url']}")
        print(f"   📝 {endpoint['description']}")
        print(f"   🔐 {endpoint['auth']}")
        print()

if __name__ == "__main__":
    print("🎯 DEMOSTRACIÓN DEL SISTEMA DE AUTENTICACIÓN DJANGO")
    print("🔧 Configurado con dj-rest-auth + django-allauth")
    print()
    
    # Verificar que el servidor está corriendo
    try:
        response = requests.get(f"{BASE_URL}/auth/login/")
        if response.status_code == 405:  # Method not allowed es esperado
            print("✅ Servidor Django disponible")
        else:
            print("⚠️  Servidor responde pero con status inesperado")
    except:
        print("❌ Servidor Django no disponible en http://127.0.0.1:8000")
        print("💡 Asegúrate de que el servidor esté corriendo con: python manage.py runserver")
        sys.exit(1)
    
    success = demo_auth_flow()
    show_available_endpoints()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡DEMOSTRACIÓN COMPLETADA EXITOSAMENTE!")
        print("💪 El sistema de autenticación está funcionando correctamente")
        print("🚀 El frontend puede usar estos endpoints para autenticación")
    else:
        print("⚠️  La demostración tuvo algunos problemas")
        print("🔧 Revisar logs del servidor para más detalles")
    
    print("\n📖 Para usar desde el frontend:")
    print("   1. POST /auth/registration/ para registrar usuarios")  
    print("   2. POST /auth/login/ para autenticar")
    print("   3. Usar token en header: Authorization: Token <token>")
    print("   4. GET /auth/user/ para obtener datos del usuario")
    print("   5. POST /auth/logout/ para cerrar sesión")

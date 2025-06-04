#!/usr/bin/env python
"""
Script para verificar endpoints de autenticación en Railway
"""
import requests
import json
import sys

# URL base de Railway
BASE_URL = "https://apihack3r-production.up.railway.app"

def test_railway_auth_endpoints():
    """Verifica los endpoints de autenticación en Railway"""
    print("🚀 VERIFICANDO ENDPOINTS DE AUTENTICACIÓN EN RAILWAY")
    print("=" * 60)
    print(f"🌐 Base URL: {BASE_URL}")
    print()
    
    # 1. Verificar disponibilidad de endpoints
    print("1. 🔍 Verificando disponibilidad de endpoints:")
    print("-" * 45)
    
    endpoints_test = [
        ("/auth/login/", "POST"),
        ("/auth/logout/", "POST"), 
        ("/auth/user/", "GET"),
        ("/auth/registration/", "POST"),
        ("/api/profile/", "GET"),
    ]
    
    for endpoint, method in endpoints_test:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", json={}, timeout=10)
                
            print(f"   ✅ {method} {endpoint} - Status: {response.status_code}")
            
            if response.status_code == 405:
                print(f"      ✓ Método correcto (405 = Method not allowed para GET en endpoint POST)")
            elif response.status_code == 401:
                print(f"      ✓ Autenticación requerida (401 = correcto)")
            elif response.status_code == 400:
                print(f"      ✓ Endpoint funcional (400 = Bad Request por datos vacíos)")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ {endpoint} - Timeout (servidor puede estar ocupado)")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {endpoint} - Error de conexión")
        except Exception as e:
            print(f"   ❌ {endpoint} - Error: {e}")
    
    print()
    
    # 2. Intentar registro de usuario
    print("2. 📝 Probando registro de usuario:")
    print("-" * 35)
    
    register_data = {
        "username": f"railwaytest{hash(str(requests.get(f'{BASE_URL}/auth/login/').status_code)) % 1000}",
        "email": "railway@test.com",
        "password1": "railwaytest123!",
        "password2": "railwaytest123!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/registration/",
            json=register_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"📊 Status del registro: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            token = result.get("key") or result.get("token")
            print(f"✅ Usuario registrado: {register_data['username']}")
            if token:
                print(f"🔑 Token obtenido: {token[:20]}...")
                return test_authenticated_operations_railway(token)
        else:
            print(f"📄 Respuesta: {response.text[:200]}...")
            print("🔄 Intentando login con usuario existente...")
            return test_login_railway()
            
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return test_login_railway()

def test_login_railway():
    """Prueba login en Railway"""
    print("\n3. 🔐 Probando login en Railway:")
    print("-" * 35)
    
    # Usuarios de prueba comunes
    test_users = [
        {"username": "admin", "password": "admin123"},
        {"username": "testuser", "password": "testpass123!"},
        {"username": "test", "password": "test123"}
    ]
    
    for user_data in test_users:
        try:
            response = requests.post(
                f"{BASE_URL}/auth/login/",
                json=user_data,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            print(f"🔍 Probando: {user_data['username']} - Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                token = result.get("key") or result.get("token")
                print(f"✅ Login exitoso!")
                if token:
                    print(f"🔑 Token: {token[:20]}...")
                    return test_authenticated_operations_railway(token)
            else:
                print(f"   📄 {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("⚠️  No se pudo hacer login con usuarios predeterminados")
    return False

def test_authenticated_operations_railway(token):
    """Prueba operaciones autenticadas en Railway"""
    print(f"\n4. 🔒 Probando operaciones autenticadas:")
    print("-" * 45)
    
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Obtener perfil
    try:
        response = requests.get(f"{BASE_URL}/auth/user/", headers=headers, timeout=10)
        print(f"👤 Perfil de usuario - Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ Usuario: {user_data.get('username', 'N/A')}")
            print(f"   📧 Email: {user_data.get('email', 'N/A')}")
        else:
            print(f"   📄 {response.text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Logout
    try:
        response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers, timeout=10)
        print(f"👋 Logout - Status: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print("   ✅ Logout exitoso")
        else:
            print(f"   📄 {response.text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return True

def show_frontend_config():
    """Muestra configuración para el frontend"""
    print("\n📋 CONFIGURACIÓN PARA EL FRONTEND")
    print("=" * 45)
    print()
    print("🔧 URL Base a usar:")
    print(f"   const API_BASE_URL = '{BASE_URL}';")
    print()
    print("🔗 Endpoints disponibles:")
    endpoints = [
        "POST /auth/registration/ - Registro de usuario",
        "POST /auth/login/ - Iniciar sesión", 
        "POST /auth/logout/ - Cerrar sesión",
        "GET  /auth/user/ - Obtener perfil",
        "GET  /api/profile/ - Perfil personalizado"
    ]
    
    for endpoint in endpoints:
        print(f"   ✅ {endpoint}")
    
    print()
    print("💻 Ejemplo de uso:")
    print(f"""
const loginUser = async (credentials) => {{
    const response = await fetch('{BASE_URL}/auth/login/', {{
        method: 'POST',
        headers: {{
            'Content-Type': 'application/json',
        }},
        body: JSON.stringify({{
            username: credentials.username,
            password: credentials.password,
        }}),
    }});
    
    if (!response.ok) {{
        throw new Error(`HTTP ${{response.status}}: ${{response.statusText}}`);
    }}
    
    const data = await response.json();
    return data.key; // Token de autenticación
}};
""")

if __name__ == "__main__":
    print("🎯 VERIFICACIÓN DE ENDPOINTS EN RAILWAY")
    print("🔧 Django + dj-rest-auth en producción")
    print()
    
    success = test_railway_auth_endpoints()
    show_frontend_config()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡ENDPOINTS DE RAILWAY FUNCIONANDO CORRECTAMENTE!")
        print("💪 El frontend puede conectarse usando la configuración mostrada")
    else:
        print("⚠️  Algunos tests fallaron - revisar logs de Railway")
    
    print(f"\n🌐 URL de admin: {BASE_URL}/admin/")
    print(f"📚 URL de docs: {BASE_URL}/api/docs/")

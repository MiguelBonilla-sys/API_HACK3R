#!/usr/bin/env python
"""
Script para probar los endpoints de autenticación de Django
"""
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_auth_endpoints():
    """Prueba los endpoints de autenticación"""
    print("🔍 Probando endpoints de autenticación...\n")
    
    # 1. Verificar que los endpoints existen
    print("1. Verificando disponibilidad de endpoints:")
    
    endpoints = [
        "/auth/login/",
        "/auth/logout/", 
        "/auth/user/",
        "/auth/registration/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"   ✅ {endpoint} - Status: {response.status_code}")
            if response.status_code == 405:
                print(f"      (Método GET no permitido - correcto para POST endpoints)")
            elif response.status_code == 401:
                print(f"      (Autenticación requerida - correcto)")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {endpoint} - Error: Servidor no disponible")
            return False
        except Exception as e:
            print(f"   ❌ {endpoint} - Error: {e}")
    
    print()
    
    # 2. Probar registro de usuario
    print("2. Probando registro de usuario:")
    register_data = {
        "username": "testuser123",
        "email": "test@example.com", 
        "password1": "testpass123!",
        "password2": "testpass123!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/registration/",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print("   ✅ Registro exitoso")
            result = response.json()
            token = result.get("key") or result.get("token")
            if token:
                print(f"   🔑 Token obtenido: {token[:20]}...")
                return test_authenticated_endpoints(token)
        else:
            print(f"   ⚠️  Registro falló: {response.text}")
            # Intentar login con usuario existente
            return test_login()
            
    except Exception as e:
        print(f"   ❌ Error en registro: {e}")
        return test_login()

def test_login():
    """Prueba el login con usuario existente"""
    print("\n3. Probando login:")
    
    # Primero intentar con superuser si existe
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            token = result.get("key") or result.get("token")
            if token:
                print(f"   ✅ Login exitoso con admin")
                print(f"   🔑 Token: {token[:20]}...")
                return test_authenticated_endpoints(token)
        
        # Si falla, intentar con testuser
        login_data["username"] = "testuser123"
        login_data["password"] = "testpass123!"
        
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("key") or result.get("token")
            if token:
                print(f"   ✅ Login exitoso con testuser")
                return test_authenticated_endpoints(token)
        
        print(f"   ⚠️  Login falló: {response.text}")
        return False
        
    except Exception as e:
        print(f"   ❌ Error en login: {e}")
        return False

def test_authenticated_endpoints(token):
    """Prueba endpoints que requieren autenticación"""
    print(f"\n4. Probando endpoints autenticados:")
    
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    # Probar perfil de usuario
    try:
        response = requests.get(f"{BASE_URL}/auth/user/", headers=headers)
        print(f"   /auth/user/ - Status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✅ Perfil obtenido: {user_data.get('username', 'N/A')}")
        else:
            print(f"   ⚠️  Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error obteniendo perfil: {e}")
    
    # Probar logout
    try:
        response = requests.post(f"{BASE_URL}/auth/logout/", headers=headers)
        print(f"   /auth/logout/ - Status: {response.status_code}")
        if response.status_code in [200, 204]:
            print("   ✅ Logout exitoso")
        else:
            print(f"   ⚠️  Error en logout: {response.text}")
    except Exception as e:
        print(f"   ❌ Error en logout: {e}")
    
    return True

def test_custom_endpoints():
    """Prueba endpoints personalizados del blog"""
    print("\n5. Probando endpoints personalizados:")
    
    custom_endpoints = [
        "/api/profile/",
        "/api/auth-status/",
    ]
    
    for endpoint in custom_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"   {endpoint} - Status: {response.status_code}")
            if response.status_code == 401:
                print(f"      (Autenticación requerida - correcto)")
            elif response.status_code == 405:
                print(f"      (Método GET no permitido - verificar método correcto)")
        except Exception as e:
            print(f"   ❌ {endpoint} - Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de endpoints de autenticación")
    print("=" * 50)
    
    success = test_auth_endpoints()
    test_custom_endpoints()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Pruebas completadas - Los endpoints están funcionando")
    else:
        print("⚠️  Algunas pruebas fallaron - Revisar configuración")

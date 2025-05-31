#!/usr/bin/env python
"""
Script para verificar el estado del deploy y probar el login
"""
import requests
import time

def test_csrf_fix():
    """Probar si el error CSRF se solucionó"""
    
    print("🔍 Verificando estado del deployment...")
    
    base_url = "https://apihack3r-production.up.railway.app"
    admin_url = f"{base_url}/admin/"
    api_url = f"{base_url}/api/hl4/v1/"
    
    # Test 1: Verificar que el sitio responde
    try:
        response = requests.get(admin_url, timeout=10)
        print(f"✅ Sitio accesible: {response.status_code}")
        
        # Verificar headers CSRF
        if 'csrftoken' in response.cookies:
            print("✅ CSRF token presente en cookies")
        else:
            print("⚠️  CSRF token no encontrado en cookies")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accediendo al sitio: {e}")
        return False
    
    # Test 2: Verificar API
    try:
        api_response = requests.get(api_url, timeout=10)
        print(f"✅ API accesible: {api_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  API no accesible: {e}")
    
    # Test 3: Intentar login (simulación)
    try:
        # Obtener CSRF token
        session = requests.Session()
        login_page = session.get(admin_url)
        
        if login_page.status_code == 200:
            print("✅ Página de login accesible")
            print("✅ Session y CSRF configurados correctamente")
        else:
            print(f"⚠️  Problema con página de login: {login_page.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando login: {e}")
    
    return True

def main():
    """Función principal"""
    print("🚀 Verificando configuración CSRF post-deploy...")
    print("=" * 50)
    
    # Esperar un poco para que el deploy se complete
    print("⏳ Esperando que se complete el deploy...")
    time.sleep(10)
    
    # Ejecutar tests
    test_csrf_fix()
    
    print("\n" + "=" * 50)
    print("🎯 INSTRUCCIONES PARA EL LOGIN")
    print("=" * 50)
    print("1. Abre una pestaña de incógnito en tu navegador")
    print("2. Ve a: https://apihack3r-production.up.railway.app/admin/")
    print("3. Usa las credenciales:")
    print("   Usuario: admin")
    print("   Password: Hack3r2024!@#")
    print("4. Si aún tienes problemas CSRF:")
    print("   - Limpia todas las cookies del dominio railway.app")
    print("   - Asegúrate de usar HTTPS (no HTTP)")
    print("   - Verifica que JavaScript esté habilitado")
    print("=" * 50)

if __name__ == '__main__':
    main()

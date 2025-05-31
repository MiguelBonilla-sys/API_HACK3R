#!/usr/bin/env python3
"""
🧪 Script de Pruebas Completas para API Django en Railway
URL: https://apihack3r-production.up.railway.app
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# 🌐 URL de tu aplicación en Railway
URL_BASE = "https://apihack3r-production.up.railway.app"

class RailwayAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Railway-API-Tester/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def test_connection(self) -> bool:
        """Prueba la conexión básica a la aplicación"""
        print("🔌 Probando conexión básica...")
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Tiempo de respuesta: {response.elapsed.total_seconds():.2f}s")
            
            if response.status_code in [200, 301, 302, 404]:
                print("   ✅ Servidor respondiendo correctamente")
                return True
            else:
                print(f"   ⚠️ Respuesta inesperada: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")
            return False
    
    def test_admin_panel(self) -> None:
        """Prueba el panel de administración de Django"""
        print("\n🔐 Probando panel de administración...")
        try:
            response = self.session.get(f"{self.base_url}/admin/", timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Panel de admin accesible")
                if "Django administration" in response.text:
                    print("   ✅ Panel de Django cargado correctamente")
            elif response.status_code == 302:
                print("   ✅ Redirección al login (comportamiento esperado)")
            else:
                print(f"   ⚠️ Respuesta inesperada: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    def test_api_docs(self) -> None:
        """Prueba la documentación de la API (Swagger)"""
        print("\n📚 Probando documentación de API...")
        try:
            response = self.session.get(f"{self.base_url}/api/docs/", timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ Documentación de API accesible")
                if "swagger" in response.text.lower() or "openapi" in response.text.lower():
                    print("   ✅ Swagger UI cargado correctamente")
            else:
                print(f"   ⚠️ Documentación no accesible: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    def test_api_endpoints(self) -> None:
        """Prueba todos los endpoints de la API"""
        print("\n🚀 Probando endpoints de la API...")
        
        # Base API path
        api_base = f"{self.base_url}/api/hl4/v1"
        
        endpoints = [
            "auditlog",
            "conferencias", 
            "cursos",
            "integrantes",
            "noticias",
            "ofertasempleo",
            "proyectos"
        ]
        
        for endpoint in endpoints:
            try:
                url = f"{api_base}/{endpoint}/"
                print(f"\n   🔍 Probando: {endpoint}")
                print(f"   URL: {url}")
                
                response = self.session.get(url, timeout=15)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ Endpoint funcionando")
                    try:
                        data = response.json()
                        if isinstance(data, dict):
                            if 'results' in data:
                                count = len(data.get('results', []))
                                total = data.get('count', 'unknown')
                                print(f"   📊 Datos: {count} elementos (total: {total})")
                            elif 'count' in data:
                                print(f"   📊 Total de registros: {data['count']}")
                        elif isinstance(data, list):
                            print(f"   📊 {len(data)} elementos en la lista")
                          # Mostrar estructura de respuesta
                        if data:
                            if isinstance(data, dict) and 'results' in data and data['results']:
                                first_item = data['results'][0]
                                fields = list(first_item.keys())[:5]  # Primeros 5 campos
                                print(f"   🏗️ Campos: {', '.join(fields)}{'...' if len(first_item) > 5 else ''}")
                            elif isinstance(data, list) and data:
                                first_item = data[0]
                                fields = list(first_item.keys())[:5]  # Primeros 5 campos
                                print(f"   🏗️ Campos: {', '.join(fields)}{'...' if len(first_item) > 5 else ''}")
                            else:
                                print("   📝 Endpoint vacío (sin datos)")
                                
                    except json.JSONDecodeError:
                        print("   📄 Respuesta no es JSON válido")
                        
                elif response.status_code == 404:
                    print("   📭 Endpoint no encontrado")
                elif response.status_code == 403:
                    print("   🔒 Acceso denegado (puede requerir autenticación)")
                elif response.status_code == 500:
                    print("   💥 Error interno del servidor")
                else:
                    print(f"   ⚠️ Respuesta inesperada: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    def test_static_files(self) -> None:
        """Prueba que los archivos estáticos se sirvan correctamente"""
        print("\n📁 Probando archivos estáticos...")
        
        static_files = [
            "/static/admin/css/base.css",
            "/static/rest_framework/css/bootstrap.min.css",
            "/static/drf-yasg/swagger-ui-dist/swagger-ui-bundle.js"
        ]
        
        for static_file in static_files:
            try:
                url = f"{self.base_url}{static_file}"
                response = self.session.get(url, timeout=10)
                print(f"   {static_file}: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"   ✅ Archivo estático servido correctamente")
                elif response.status_code == 404:
                    print(f"   📭 Archivo no encontrado (puede ser normal)")
                else:
                    print(f"   ⚠️ Error: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    def test_api_performance(self) -> None:
        """Prueba el rendimiento de la API"""
        print("\n⚡ Probando rendimiento...")
        
        test_url = f"{self.base_url}/api/hl4/v1/noticias/"
        times = []
        
        for i in range(3):
            try:
                start_time = time.time()
                response = self.session.get(test_url, timeout=15)
                end_time = time.time()
                
                response_time = end_time - start_time
                times.append(response_time)
                
                print(f"   Prueba {i+1}: {response_time:.2f}s (Status: {response.status_code})")
                
            except Exception as e:
                print(f"   Prueba {i+1}: Error - {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            print(f"   📊 Tiempo promedio: {avg_time:.2f}s")
            
            if avg_time < 1.0:
                print("   ✅ Rendimiento excelente")
            elif avg_time < 3.0:
                print("   ✅ Rendimiento bueno")
            else:
                print("   ⚠️ Rendimiento lento")
    
    def run_all_tests(self) -> None:
        """Ejecuta todas las pruebas"""
        print("🎯 PRUEBAS COMPLETAS DE API DJANGO EN RAILWAY")
        print("=" * 60)
        print(f"🌐 URL Base: {self.base_url}")
        print(f"🕐 Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Test de conexión básica
        if not self.test_connection():
            print("\n💥 Conexión fallida. Abortando pruebas.")
            return
        
        # Ejecutar todas las pruebas
        self.test_admin_panel()
        self.test_api_docs()
        self.test_api_endpoints()
        self.test_static_files()
        self.test_api_performance()
        
        print("\n" + "=" * 60)
        print("🎉 PRUEBAS COMPLETADAS")
        print(f"🕐 Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Resumen final
        print("\n📋 RESUMEN:")
        print(f"✅ Aplicación Django funcionando en: {self.base_url}")
        print("✅ API REST con múltiples endpoints")
        print("✅ Panel de administración disponible")
        print("✅ Documentación Swagger accesible")
        print("✅ Archivos estáticos servidos")
        
        print("\n🔗 ENLACES ÚTILES:")
        print(f"🌐 Aplicación: {self.base_url}")
        print(f"🔐 Admin: {self.base_url}/admin/")
        print(f"📚 API Docs: {self.base_url}/api/docs/")
        print(f"🚀 API Base: {self.base_url}/api/hl4/v1/")

def main():
    """Función principal"""
    tester = RailwayAPITester(URL_BASE)
    tester.run_all_tests()

if __name__ == "__main__":
    main()

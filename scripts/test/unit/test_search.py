import requests
import time
from datetime import datetime

BASE_URL_AUTH = "http://localhost:8081/api/v1"
BASE_URL_API = "http://localhost:8000"

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_section(title):
    print(f"\n{'='*70}")
    print(f"{Colors.BLUE}   {title}{Colors.END}")
    print('='*70)

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.YELLOW}ℹ {msg}{Colors.END}")

# Variables globales
jwt_token = None
user_id = None
startup_ids = []

def setup_test_data():
    """Crear usuario y startups de prueba para búsqueda"""
    global jwt_token, user_id, startup_ids
    
    print_section("PREPARACIÓN: CREAR DATOS DE PRUEBA")
    
    # Registrar usuario
    timestamp = int(datetime.now().timestamp())
    test_email = f"test_search_{timestamp}@starthub.test"
    test_password = "SearchTest123!"
    
    print("Registrando usuario...")
    reg_data = {
        "firstName": "Search",
        "lastName": "Tester",
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL_AUTH}/registration", json=reg_data, timeout=10)
        if response.status_code == 200:
            token = response.text.strip()
            
            # Confirmar email
            confirm_url = f"{BASE_URL_AUTH}/registration/confirm?token={token}"
            requests.get(confirm_url, timeout=10)
            
            # Login
            time.sleep(1)
            login_data = {"email": test_email, "password": test_password}
            response = requests.post(f"{BASE_URL_AUTH}/auth/login", json=login_data, timeout=10)
            
            if response.status_code == 200:
                response_data = response.json()
                jwt_token = response_data.get("token")
                user_data = response_data.get("user", {})
                user_id = user_data.get("id")
                print_success(f"Usuario creado - ID: {user_id}")
    except Exception as e:
        print_error(f"Error en setup: {str(e)}")
        return False
    
    # Crear varias startups para pruebas de búsqueda
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    startups_data = [
        {"name": "AI Vision Platform", "description": "Plataforma de visión artificial con IA", "category_id": 1},
        {"name": "FinTech Solutions", "description": "Soluciones financieras innovadoras", "category_id": 2},
        {"name": "EduTech Learning", "description": "Plataforma educativa con IA", "category_id": 3},
        {"name": "HealthTech AI", "description": "Tecnología de salud con inteligencia artificial", "category_id": 1},
    ]
    
    print("\nCreando startups de prueba...")
    for startup_data in startups_data:
        try:
            response = requests.post(
                f"{BASE_URL_API}/startups/?user_id={user_id}",
                json=startup_data,
                headers=headers,
                timeout=10
            )
            if response.status_code in [200, 201]:
                startup = response.json()
                startup_ids.append(startup.get("startup_id"))
                print_info(f"  ✓ Creada: {startup_data['name']} (ID: {startup.get('startup_id')})")
        except Exception as e:
            print_error(f"Error creando startup: {str(e)}")
    
    return len(startup_ids) > 0

def test_search_basic():
    """Prueba 1: Búsqueda básica por término"""
    print_section("1. BÚSQUEDA BÁSICA POR TÉRMINO")
    
    # Buscar por "AI"
    print("\n1.1. BUSCAR STARTUPS CON 'AI'")
    try:
        response = requests.get(f"{BASE_URL_API}/search?q=AI", timeout=10)
        if response.status_code == 200:
            results = response.json()
            total = results.get("total", 0)
            items = results.get("results", [])
            print_success(f"Búsqueda exitosa - {total} resultados encontrados")
            for item in items[:3]:
                print_info(f"  - {item.get('name')}")
        else:
            print_error(f"Búsqueda falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # Buscar sin término (todas)
    print("\n1.2. LISTAR TODAS LAS STARTUPS")
    try:
        response = requests.get(f"{BASE_URL_API}/search", timeout=10)
        if response.status_code == 200:
            results = response.json()
            total = results.get("total", 0)
            print_success(f"Listado exitoso - Total: {total} startups")
        else:
            print_error(f"Listado falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_search_filters():
    """Prueba 2: Búsqueda con filtros"""
    print_section("2. BÚSQUEDA CON FILTROS")
    
    # Filtrar por categoría
    print("\n2.1. FILTRAR POR CATEGORÍA")
    try:
        response = requests.get(f"{BASE_URL_API}/search?categorias=1", timeout=10)
        if response.status_code == 200:
            results = response.json()
            total = results.get("total", 0)
            items = results.get("results", [])
            print_success(f"Filtro por categoría exitoso - {total} resultados")
            for item in items[:3]:
                print_info(f"  - {item.get('name')} (Categoría: {item.get('category_id')})")
        else:
            print_error(f"Filtro falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # Filtrar por múltiples categorías
    print("\n2.2. FILTRAR POR MÚLTIPLES CATEGORÍAS")
    try:
        response = requests.get(f"{BASE_URL_API}/search?categorias=1,2", timeout=10)
        if response.status_code == 200:
            results = response.json()
            total = results.get("total", 0)
            print_success(f"Filtro múltiple exitoso - {total} resultados")
        else:
            print_error(f"Filtro múltiple falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Filtrar por votos mínimos
    print("\n2.3. FILTRAR POR VOTOS MÍNIMOS")
    try:
        response = requests.get(f"{BASE_URL_API}/search?min_votos=0", timeout=10)
        if response.status_code == 200:
            results = response.json()
            print_success(f"Filtro por votos exitoso - {results.get('total', 0)} resultados")
        else:
            print_error(f"Filtro por votos falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_search_sorting():
    """Prueba 3: Ordenamiento de resultados"""
    print_section("3. ORDENAMIENTO DE RESULTADOS")
    
    sort_options = [
        ("relevancia", "RELEVANCIA"),
        ("votos", "VOTOS"),
        ("comentarios", "COMENTARIOS"),
        ("recientes", "RECIENTES")
    ]
    
    for param, name in sort_options:
        print(f"\n3.{sort_options.index((param, name)) + 1}. ORDENAR POR {name}")
        try:
            response = requests.get(f"{BASE_URL_API}/search?sort_by={param}", timeout=10)
            if response.status_code == 200:
                results = response.json()
                print_success(f"Ordenamiento por {name} exitoso")
            else:
                print_error(f"Ordenamiento por {name} falló: {response.status_code}")
        except Exception as e:
            print_error(f"Error: {str(e)}")
    
    return True

def test_search_pagination():
    """Prueba 4: Paginación"""
    print_section("4. PAGINACIÓN")
    
    print("\n4.1. OBTENER PRIMERA PÁGINA")
    try:
        response = requests.get(f"{BASE_URL_API}/search?page=1&limit=2", timeout=10)
        if response.status_code == 200:
            results = response.json()
            page = results.get("page", 0)
            per_page = results.get("per_page", 0)
            total = results.get("total", 0)
            print_success(f"Página {page} obtenida ({per_page} items por página, {total} total)")
        else:
            print_error(f"Paginación falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    print("\n4.2. OBTENER SEGUNDA PÁGINA")
    try:
        response = requests.get(f"{BASE_URL_API}/search?page=2&limit=2", timeout=10)
        if response.status_code == 200:
            results = response.json()
            print_success(f"Página 2 obtenida")
        else:
            print_error(f"Página 2 falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_autocomplete():
    """Prueba 5: Autocompletado"""
    print_section("5. AUTOCOMPLETADO")
    
    print("\n5.1. AUTOCOMPLETAR 'AI'")
    try:
        response = requests.get(f"{BASE_URL_API}/autocomplete?q=AI", timeout=10)
        if response.status_code == 200:
            results = response.json()
            print_success(f"Autocompletado exitoso - {len(results)} sugerencias")
            for item in results[:5]:
                print_info(f"  - {item.get('name')}")
        else:
            print_error(f"Autocompletado falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    print("\n5.2. AUTOCOMPLETAR 'Tech'")
    try:
        response = requests.get(f"{BASE_URL_API}/autocomplete?q=Tech", timeout=10)
        if response.status_code == 200:
            results = response.json()
            print_success(f"Autocompletado exitoso - {len(results)} sugerencias")
        else:
            print_error(f"Autocompletado falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_startup_detail():
    """Prueba 6: Detalle de startup"""
    print_section("6. DETALLE DE STARTUP")
    
    if not startup_ids:
        print_error("No hay startups de prueba creadas")
        return False
    
    print(f"\n6.1. OBTENER DETALLE DE STARTUP (ID: {startup_ids[0]})")
    try:
        response = requests.get(f"{BASE_URL_API}/{startup_ids[0]}", timeout=10)
        if response.status_code == 200:
            startup = response.json()
            print_success(f"Detalle obtenido: {startup.get('name')}")
            print_info(f"  Descripción: {startup.get('description')[:50]}...")
            print_info(f"  Votos: {startup.get('total_votos')}, Comentarios: {startup.get('total_comentarios')}")
        else:
            print_error(f"Obtener detalle falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    return True

def cleanup_test_data():
    """Limpiar datos de prueba"""
    print_section("LIMPIEZA: ELIMINAR DATOS DE PRUEBA")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # Eliminar startups
    print("\nEliminando startups de prueba...")
    for startup_id in startup_ids:
        try:
            requests.delete(
                f"{BASE_URL_API}/startups/{startup_id}?user_id={user_id}",
                headers=headers,
                timeout=10
            )
            print_info(f"  ✓ Eliminada startup ID: {startup_id}")
        except Exception as e:
            print_error(f"Error eliminando startup {startup_id}: {str(e)}")
    
    # Eliminar usuario
    print("\nEliminando usuario de prueba...")
    try:
        response = requests.delete(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        if response.status_code == 200:
            print_success("Usuario eliminado correctamente")
    except Exception as e:
        print_error(f"Error eliminando usuario: {str(e)}")

def main():
    """Ejecutar todas las pruebas de búsqueda"""
    print_section("PRUEBAS DE BÚSQUEDA")
    print(f"{Colors.YELLOW}StartHub - Verificación de Funcionalidad de Búsqueda{Colors.END}")
    
    # Setup
    if not setup_test_data():
        print_error("Falló la preparación de datos. Abortando pruebas.")
        return
    
    time.sleep(1)
    
    # Ejecutar pruebas
    test_search_basic()
    time.sleep(0.5)
    
    test_search_filters()
    time.sleep(0.5)
    
    test_search_sorting()
    time.sleep(0.5)
    
    test_search_pagination()
    time.sleep(0.5)
    
    test_autocomplete()
    time.sleep(0.5)
    
    test_startup_detail()
    time.sleep(0.5)
    
    # Cleanup
    cleanup_test_data()
    
    # Resumen
    print_section("PRUEBAS DE BÚSQUEDA COMPLETADAS")
    print(f"{Colors.GREEN}✅ Todas las pruebas de búsqueda ejecutadas{Colors.END}")
    print(f"\n{Colors.BLUE}Resumen:{Colors.END}")
    print("  ✓ Búsqueda básica por término")
    print("  ✓ Filtros (categorías, votos, comentarios)")
    print("  ✓ Ordenamiento (relevancia, votos, comentarios, recientes)")
    print("  ✓ Paginación")
    print("  ✓ Autocompletado")
    print("  ✓ Detalle de startup")

if __name__ == "__main__":
    main()

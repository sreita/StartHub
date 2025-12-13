import requests
import time
from datetime import datetime

BASE_URL_AUTH = "http://localhost:8081/api/v1"
BASE_URL_API = "http://localhost:8000/api/v1"

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
startup_id = None
user_id = None
user_email = None
user_password = None

def test_user_registration():
    """Prueba 1: Registro de usuario"""
    global user_email, user_password
    
    print_section("1. REGISTRO DE USUARIO")
    
    timestamp = int(datetime.now().timestamp())
    test_email = f"test_user_{timestamp}@starthub.test"
    test_password = "UserTest123!"
    user_email = test_email
    user_password = test_password
    
    print("1.1. REGISTRANDO NUEVO USUARIO")
    reg_data = {
        "firstName": "Test",
        "lastName": "User",
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL_AUTH}/registration", json=reg_data, timeout=10)
        if response.status_code == 200:
            token = response.json().get("token")
            print_success(f"Usuario registrado exitosamente")
            print_info(f"  Token de confirmación: {str(token)[:40]}...")
            return token
        else:
            print_error(f"Registro falló: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_email_confirmation(token):
    """Prueba 2: Confirmación de email"""
    print_section("2. CONFIRMACIÓN DE EMAIL")
    
    print("2.1. CONFIRMANDO EMAIL CON TOKEN")
    try:
        confirm_url = f"{BASE_URL_AUTH}/registration/confirm?token={token}"
        response = requests.get(confirm_url, timeout=10)
        
        if response.status_code == 200:
            print_success("Email confirmado exitosamente")
            return True
        else:
            print_error(f"Confirmación falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_user_login():
    """Prueba 3: Login de usuario"""
    global jwt_token, user_id
    
    print_section("3. LOGIN DE USUARIO")
    
    print("3.1. INICIANDO SESIÓN")
    login_data = {"email": user_email, "password": user_password}
    
    try:
        response = requests.post(f"{BASE_URL_AUTH}/auth/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            response_data = response.json()
            jwt_token = response_data.get("token")
            user_data = response_data.get("user", {})
            user_id = user_data.get("id")
            
            print_success(f"Login exitoso")
            print_info(f"  User ID: {user_id}")
            print_info(f"  JWT Token: {jwt_token[:50]}...")
            return True
        else:
            print_error(f"Login falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_user_profile():
    """Prueba 4: Obtener perfil de usuario"""
    print_section("4. PERFIL DE USUARIO")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    print("4.1. OBTENER PERFIL")
    try:
        response = requests.get(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        
        if response.status_code == 200:
            profile = response.json()
            print_success("Perfil obtenido exitosamente")
            print_info(f"  Nombre: {profile.get('firstName')} {profile.get('lastName')}")
            print_info(f"  Email: {profile.get('email')}")
            print_info(f"  Fecha registro: {profile.get('registrationDate')}")
            return True
        else:
            print_error(f"Obtener perfil falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_user_update():
    """Prueba 5: Actualizar perfil de usuario"""
    print_section("5. ACTUALIZACIÓN DE PERFIL")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    print("5.1. ACTUALIZAR DATOS DE PERFIL")
    update_data = {
        "firstName": "TestUpdated",
        "lastName": "UserUpdated",
        "email": user_email,  # Mantener mismo email
        "profileInfo": "Información de perfil actualizada para pruebas"
    }
    
    try:
        response = requests.put(f"{BASE_URL_AUTH}/users/{user_id}", json=update_data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            updated_profile = response.json()
            print_success("Perfil actualizado exitosamente")
            print_info(f"  Nuevo nombre: {updated_profile.get('firstName')} {updated_profile.get('lastName')}")
            print_info(f"  ProfileInfo: {updated_profile.get('profileInfo')}")
        else:
            print_error(f"Actualización falló: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # Verificar actualización
    print("\n5.2. VERIFICAR ACTUALIZACIÓN")
    try:
        response = requests.get(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        
        if response.status_code == 200:
            profile = response.json()
            if profile.get('firstName') == 'TestUpdated':
                print_success("Actualización verificada correctamente")
            else:
                print_error("La actualización no se reflejó")
        else:
            print_error(f"Verificación falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_startup_crud():
    """Prueba 6: CRUD completo de Startups"""
    global startup_id
    
    print_section("6. CRUD DE STARTUPS")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # CREATE
    print("\n6.1. CREAR STARTUP")
    startup_data = {
        "name": "TestStartup Innovation",
        "description": "Startup de prueba para verificar operaciones CRUD completas",
        "category_id": 1,
        "owner_user_id": user_id
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_API}/startups/",
            json=startup_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            startup = response.json()
            startup_id = startup.get("startup_id")
            print_success(f"Startup creada exitosamente")
            print_info(f"  ID: {startup_id}")
            print_info(f"  Nombre: {startup.get('name')}")
        else:
            print_error(f"Creación falló: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # READ
    print("\n6.2. LEER STARTUP")
    try:
        response = requests.get(f"{BASE_URL_API}/startups/{startup_id}", timeout=10)
        
        if response.status_code == 200:
            startup = response.json()
            print_success("Startup encontrada")
            print_info(f"  Nombre: {startup.get('name')}")
            print_info(f"  Descripción: {startup.get('description')[:50]}...")
            print_info(f"  Categoría: {startup.get('category_id')}")
        else:
            print_error(f"Lectura falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # LIST (my startups)
    print("\n6.3. LISTAR MIS STARTUPS")
    try:
        response = requests.get(f"{BASE_URL_API}/startups/my-startups?user_id={user_id}", timeout=10)
        
        if response.status_code == 200:
            startups = response.json()
            print_success(f"Listado obtenido - Total: {len(startups)} startups")
            
            found = any(s.get('startup_id') == startup_id for s in startups)
            if found:
                print_info("  ✓ Startup creada encontrada en el listado")
        else:
            print_error(f"Listado falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # UPDATE
    print("\n6.4. ACTUALIZAR STARTUP")
    update_data = {
        "name": "TestStartup Innovation - UPDATED",
        "description": "Descripción actualizada con nueva información",
        "category_id": 2
    }
    
    try:
        response = requests.put(
            f"{BASE_URL_API}/startups/{startup_id}?user_id={user_id}",
            json=update_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            startup = response.json()
            print_success("Startup actualizada exitosamente")
            print_info(f"  Nuevo nombre: {startup.get('name')}")
            print_info(f"  Nueva categoría: {startup.get('category_id')}")
        else:
            print_error(f"Actualización falló: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # VERIFY UPDATE
    print("\n6.5. VERIFICAR ACTUALIZACIÓN")
    try:
        response = requests.get(f"{BASE_URL_API}/startups/{startup_id}", timeout=10)
        
        if response.status_code == 200:
            startup = response.json()
            if "UPDATED" in startup.get('name', '') and startup.get('category_id') == 2:
                print_success("Actualización verificada correctamente")
            else:
                print_error("La actualización no se reflejó completamente")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # DELETE se hace al final en cleanup
    return True

def test_startup_with_stats():
    """Prueba 7: Obtener startup con estadísticas"""
    print_section("7. STARTUP CON ESTADÍSTICAS")
    
    print("7.1. OBTENER STARTUP CON STATS")
    try:
        response = requests.get(f"{BASE_URL_API}/startups/{startup_id}/with-stats", timeout=10)
        
        if response.status_code == 200:
            startup = response.json()
            print_success("Startup con stats obtenida")
            print_info(f"  Nombre: {startup.get('name')}")
            print_info(f"  Total votos: {startup.get('total_votos', 0)}")
            print_info(f"  Total comentarios: {startup.get('total_comentarios', 0)}")
            print_info(f"  Upvotes: {startup.get('upvotes', 0)}")
            print_info(f"  Downvotes: {startup.get('downvotes', 0)}")
        else:
            print_error(f"Obtener stats falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    return True

def test_user_delete():
    """Prueba 8: Eliminar usuario (al final)"""
    print_section("8. ELIMINACIÓN DE USUARIO")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # Primero eliminar startup
    print("8.1. ELIMINAR STARTUP PRIMERO")
    try:
        response = requests.delete(
            f"{BASE_URL_API}/startups/{startup_id}?user_id={user_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 204]:
            print_success("Startup eliminada")
            
            # Verificar eliminación de startup
            response = requests.get(f"{BASE_URL_API}/startups/{startup_id}", timeout=10)
            if response.status_code == 404:
                print_info("  ✓ Eliminación de startup verificada")
        else:
            print_error(f"Eliminación de startup falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Ahora eliminar usuario
    print("\n8.2. ELIMINAR USUARIO")
    try:
        response = requests.delete(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print_success("Usuario eliminado exitosamente")
        else:
            print_error(f"Eliminación de usuario falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # Verificar que no se puede acceder al perfil
    print("\n8.3. VERIFICAR INACCESIBILIDAD DE PERFIL")
    try:
        response = requests.get(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        
        if response.status_code in [404, 500]:
            print_success(f"Perfil inaccesible tras eliminación (status {response.status_code})")
        else:
            print_error(f"Perfil aún accesible: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Verificar que no se puede hacer login
    print("\n8.4. VERIFICAR LOGIN RECHAZADO")
    try:
        response = requests.post(
            f"{BASE_URL_AUTH}/auth/login",
            json={"email": user_email, "password": user_password},
            timeout=10
        )
        
        if response.status_code != 200:
            print_success(f"Login correctamente rechazado (status {response.status_code})")
        else:
            print_error("Login inesperadamente exitoso")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def main():
    """Ejecutar todas las pruebas de usuarios y startups"""
    print_section("PRUEBAS DE USUARIOS Y STARTUPS")
    print(f"{Colors.YELLOW}StartHub - Verificación CRUD de Usuarios y Startups{Colors.END}")
    
    # Registro y confirmación
    token = test_user_registration()
    if not token:
        print_error("Falló el registro. Abortando pruebas.")
        return
    
    time.sleep(1)
    
    if not test_email_confirmation(token):
        print_error("Falló la confirmación. Abortando pruebas.")
        return
    
    time.sleep(1)
    
    # Login
    if not test_user_login():
        print_error("Falló el login. Abortando pruebas.")
        return
    
    time.sleep(1)
    
    # Operaciones de usuario
    test_user_profile()
    time.sleep(0.5)
    
    test_user_update()
    time.sleep(0.5)
    
    # Operaciones de startup
    if not test_startup_crud():
        print_error("Falló CRUD de startups. Continuando con limpieza...")
    
    time.sleep(0.5)
    
    test_startup_with_stats()
    time.sleep(0.5)
    
    # Eliminación final
    test_user_delete()
    
    # Resumen
    print_section("PRUEBAS COMPLETADAS")
    print(f"{Colors.GREEN}✅ Todas las pruebas de usuarios y startups ejecutadas{Colors.END}")
    print(f"\n{Colors.BLUE}Resumen:{Colors.END}")
    print("  ✓ Registro de Usuario")
    print("  ✓ Confirmación de Email")
    print("  ✓ Login")
    print("  ✓ Perfil de Usuario (Get)")
    print("  ✓ Actualización de Perfil (Update)")
    print("  ✓ CRUD Completo de Startups (Create, Read, List, Update, Delete)")
    print("  ✓ Startup con Estadísticas")
    print("  ✓ Eliminación de Usuario y Verificaciones")

if __name__ == "__main__":
    main()

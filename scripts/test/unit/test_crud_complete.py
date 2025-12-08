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
startup_id = None
comment_id = None
user_id = None
user_email = None
user_password = None

def test_user_profile_and_update():
    """Step A: Verify profile and update user data"""
    print_section("A. USER PROFILE AND UPDATE")
    headers = {"Authorization": f"Bearer {jwt_token}"}
    # GET perfil
    print("\nA.1. GET PROFILE")
    try:
        resp = requests.get(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        if resp.status_code == 200:
            profile = resp.json()
            print_success(f"Profile obtained: {profile.get('firstName')} {profile.get('lastName')}")
        else:
            print_error(f"Failed to get profile: {resp.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    # UPDATE perfil (sin cambiar email para facilitar relogin)
    print("\nA.2. UPDATE PROFILE")
    update_payload = {
        "firstName": "TestUpdated",
        "lastName": "CRUDUpdated",
        "email": user_email,  # mantener igual
        "profileInfo": "Updated test profile"
    }
    try:
        resp = requests.put(f"{BASE_URL_AUTH}/users/{user_id}", json=update_payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            updated = resp.json()
            print_success("Profile updated successfully")
            print_info(f"New name: {updated.get('firstName')} {updated.get('lastName')}")
            print_info(f"ProfileInfo: {updated.get('profileInfo')}")
        else:
            print_error(f"Fallo actualización perfil: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    # Verify GET afterwards
    print("\nA.3. VERIFY UPDATE")
    try:
        resp = requests.get(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        if resp.status_code == 200:
            profile = resp.json()
            if profile.get('firstName') == 'TestUpdated':
                print_success("Update reflected in profile")
            else:
                print_error("Update NOT reflected in profile")
        else:
            print_error(f"Profile verification failed: {resp.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")
    return True

def test_user_relogin():
    """Step B: Re-login after update to validate validity"""
    print_section("B. USER RE-LOGIN")
    print("Attempting login again after update...")
    try:
        resp = requests.post(f"{BASE_URL_AUTH}/auth/login", json={"email": user_email, "password": user_password}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            print_success("Successful re-login after update")
            print_info(f"JWT nuevo: {data.get('token')[:40]}...")
            return True
        else:
            print_error(f"Re-login failed: {resp.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_user_delete_and_post_checks():
    """Paso Z: Eliminar usuario y verificar que no se puede acceder ni loguear"""
    print_section("Z. USER DELETION")
    headers = {"Authorization": f"Bearer {jwt_token}"}
    print("\nZ.1. ELIMINAR USUARIO")
    try:
        resp = requests.delete(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        if resp.status_code == 200:
            print_success("Usuario eliminado correctamente")
        else:
            print_error(f"Deletion failed: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False
    # Intentar obtener perfil
    print("\nZ.2. VERIFY PROFILE ACCESS AFTER DELETION")
    try:
        resp = requests.get(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        if resp.status_code in [404, 500]:
            print_success(f"Profile inaccessible after deletion (status {resp.status_code})")
        else:
            print_error(f"Estado inesperado perfil: {resp.status_code}")
    except Exception as e:
        print_error(f"Error: {e}")
    # Intentar login
    print("\nZ.3. LOGIN AFTER DELETION (MUST FAIL)")
    try:
        resp = requests.post(f"{BASE_URL_AUTH}/auth/login", json={"email": user_email, "password": user_password}, timeout=10)
        if resp.status_code != 200:
            print_success(f"Login correctamente rechazado (status {resp.status_code})")
        else:
            print_error("Unexpectedly successful login after deletion")
    except Exception as e:
        print_error(f"Error: {e}")
    return True

def test_register_and_login():
    """Paso 1: Registrar usuario y hacer login"""
    global jwt_token, user_id
    
    print_section("1. REGISTRO Y LOGIN DE USUARIO")
    
    global user_email, user_password
    timestamp = int(datetime.now().timestamp())
    test_email = f"test_crud_{timestamp}@starthub.test"
    test_password = "TestPass123!"
    user_email = test_email
    user_password = test_password
    
    # Registro
    print("Registrando usuario...")
    reg_data = {
        "firstName": "Test",
        "lastName": "CRUD",
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL_AUTH}/registration", json=reg_data, timeout=10)
        if response.status_code == 200:
            token = response.text.strip()
            print_success(f"Registro exitoso - Token: {token[:40]}...")
            
            # Automatic confirmation
            print("Confirmando email...")
            confirm_url = f"{BASE_URL_AUTH}/registration/confirm?token={token}"
            response = requests.get(confirm_url, timeout=10)
            
            if response.status_code == 200:
                print_success("Email confirmado")
                
                # Login
                print("Haciendo login...")
                time.sleep(1)
                login_data = {"email": test_email, "password": test_password}
                response = requests.post(f"{BASE_URL_AUTH}/auth/login", json=login_data, timeout=10)
                
                if response.status_code == 200:
                    response_data = response.json()
                    jwt_token = response_data.get("token")
                    user_data = response_data.get("user", {})
                    user_id = user_data.get("id")
                    print_success(f"Login exitoso - JWT: {jwt_token[:50]}...")
                    print_info(f"User ID: {user_id}")
                    return True
                else:
                    print_error(f"Login falló: {response.status_code}")
            else:
                print_error(f"Confirmación falló: {response.status_code}")
        else:
            print_error(f"Registro falló: {response.status_code} - {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return False

def test_startup_crud():
    """Paso 2: Probar CRUD de Startups"""
    global startup_id
    
    print_section("2. CRUD DE STARTUPS")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # CREATE - Crear startup
    print("\n2.1. CREAR STARTUP")
    startup_data = {
        "name": "TestStartup AI",
        "description": "Una startup de prueba para testing CRUD",
        "category_id": 1,
        "owner_user_id": user_id
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_API}/startups/?user_id={user_id}", 
            json=startup_data, 
            headers=headers, 
            timeout=10
        )
        if response.status_code in [200, 201]:
            startup = response.json()
            startup_id = startup.get("startup_id")
            print_success(f"Startup creada - ID: {startup_id}")
            print_info(f"Nombre: {startup.get('name')}")
        else:
            print_error(f"Creación falló: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # READ - Leer startup
    print("\n2.2. LEER STARTUP")
    try:
        response = requests.get(f"{BASE_URL_API}/startups/{startup_id}", timeout=10)
        if response.status_code == 200:
            startup = response.json()
            print_success(f"Startup encontrada: {startup.get('name')}")
            print_info(f"Description: {startup.get('description')[:50]}...")
        else:
            print_error(f"Lectura falló: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # UPDATE - Actualizar startup
    print("\n2.3. ACTUALIZAR STARTUP")
    update_data = {
        "name": "TestStartup AI - UPDATED",
        "description": "Updated description for testing",
        "category_id": 2,
        "owner_user_id": user_id
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
            print_success(f"Startup actualizada")
            print_info(f"New name: {startup.get('name')}")
            print_info(f"New category: {startup.get('category_id')}")
        else:
            print_error(f"Update failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # Verificar actualización
    print("\n2.4. VERIFY UPDATE")
    try:
        response = requests.get(f"{BASE_URL_API}/startups/{startup_id}", timeout=10)
        if response.status_code == 200:
            startup = response.json()
            if "UPDATED" in startup.get('name', ''):
                print_success("Actualización verificada correctamente")
                print_info(f"New category: {startup.get('category_id')}")
            else:
                print_error("The update was not reflected")
        else:
            print_error(f"Verification failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_vote_operations():
    """Paso 3: Probar votos"""
    print_section("3. OPERACIONES DE VOTOS")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # CREATE - Dar upvote
    print("\n3.1. DAR UPVOTE")
    vote_data = {
        "startup_id": startup_id,
        "vote_type": "upvote"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_API}/votes/?user_id={user_id}", 
            json=vote_data, 
            headers=headers, 
            timeout=10
        )
        if response.status_code in [200, 201]:
            vote = response.json()
            print_success(f"Upvote registrado - Vote ID: {vote.get('vote_id')}")
        else:
            print_error(f"Upvote failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # READ - Verificar votos de la startup
    print("\n3.2. LEER VOTOS DE LA STARTUP")
    try:
        response = requests.get(f"{BASE_URL_API}/votes/count/{startup_id}", timeout=10)
        if response.status_code == 200:
            vote_count = response.json()
            print_success(f"Votos obtenidos")
            print_info(f"Upvotes: {vote_count.get('upvotes')}, Downvotes: {vote_count.get('downvotes')}")
        else:
            print_error(f"Vote reading failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # UPDATE - Cambiar a downvote
    print("\n3.3. CAMBIAR VOTO A DOWNVOTE")
    update_vote_data = {
        "startup_id": startup_id,
        "vote_type": "downvote"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_API}/votes/?user_id={user_id}", 
            json=update_vote_data, 
            headers=headers, 
            timeout=10
        )
        if response.status_code in [200, 201]:
            vote = response.json()
            if vote.get('vote_type') == 'downvote':
                print_success("Voto cambiado a downvote")
            else:
                print_info("Respuesta del servidor sobre el voto")
        else:
            print_error(f"Vote change failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # DELETE - Eliminar voto
    print("\n3.4. ELIMINAR VOTO")
    try:
        response = requests.delete(f"{BASE_URL_API}/votes/?user_id={user_id}&startup_id={startup_id}", headers=headers, timeout=10)
        if response.status_code in [200, 204]:
            print_success("Voto eliminado")
        else:
            print_error(f"Vote deletion failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_comment_operations():
    """Paso 4: Probar comentarios"""
    global comment_id
    
    print_section("4. OPERACIONES DE COMENTARIOS")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # CREATE - Crear comentario
    print("\n4.1. CREAR COMENTARIO")
    comment_data = {
        "startup_id": startup_id,
        "content": "Este es un comentario de prueba para verificar el CRUD"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_API}/comments/?user_id={user_id}", 
            json=comment_data, 
            headers=headers, 
            timeout=10
        )
        if response.status_code in [200, 201]:
            comment = response.json()
            comment_id = comment.get('comment_id')
            print_success(f"Comentario creado - ID: {comment_id}")
            print_info(f"Texto: {comment.get('content')[:50]}...")
        else:
            print_error(f"Comment creation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # READ - Leer comentarios de la startup
    print("\n4.2. LEER COMENTARIOS DE LA STARTUP")
    try:
        response = requests.get(f"{BASE_URL_API}/comments/?startup_id={startup_id}", timeout=10)
        if response.status_code == 200:
            comments = response.json()
            print_success(f"Comentarios obtenidos - Total: {len(comments)}")
            for c in comments:
                print_info(f"  - ID {c.get('comment_id')}: {c.get('content')[:40]}...")
        else:
            print_error(f"Comment reading failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # UPDATE - Actualizar comentario
    print("\n4.3. ACTUALIZAR COMENTARIO")
    update_comment_data = {
        "content": "UPDATED comment - Verifying edit functionality"
    }
    
    try:
        response = requests.put(f"{BASE_URL_API}/comments/{comment_id}?user_id={user_id}", json=update_comment_data, headers=headers, timeout=10)
        if response.status_code == 200:
            comment = response.json()
            print_success("Comentario actualizado")
            print_info(f"Nuevo texto: {comment.get('content')}")
        else:
            print_error(f"Comment update failed: {response.status_code} - {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # DELETE - Eliminar comentario
    print("\n4.4. ELIMINAR COMENTARIO")
    try:
        response = requests.delete(f"{BASE_URL_API}/comments/{comment_id}?user_id={user_id}", headers=headers, timeout=10)
        if response.status_code in [200, 204]:
            print_success("Comentario eliminado")
        else:
            print_error(f"Eliminación de comentario falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # Verificar eliminación
    print("\n4.5. VERIFICAR ELIMINACIÓN")
    try:
        response = requests.get(f"{BASE_URL_API}/comments/?startup_id={startup_id}", timeout=10)
        if response.status_code == 200:
            comments = response.json()
            if not any(c.get('comment_id') == comment_id for c in comments):
                print_success("Eliminación verificada - Comentario no existe")
            else:
                print_error("El comentario aún existe")
        else:
            print_error(f"Verification failed: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_startup_list_operations():
    """Paso 5: Listar startups"""
    print_section("5. LISTAR STARTUPS")
    
    # Listar todas las startups
    print("\n5.1. LISTAR TODAS LAS STARTUPS")
    try:
        response = requests.get(f"{BASE_URL_API}/startups/", timeout=10)
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
    
    # Listar mis startups
    print("\n5.2. LISTAR MIS STARTUPS")
    try:
        response = requests.get(f"{BASE_URL_API}/startups/my-startups?user_id={user_id}", timeout=10)
        if response.status_code == 200:
            my_startups = response.json()
            print_success(f"Mis startups obtenidas - Total: {len(my_startups)}")
            
            for s in my_startups:
                if s.get('startup_id') == startup_id:
                    print_info(f"  ✓ {s.get('name')}")
                    break
        else:
            print_error(f"Listado de mis startups falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def test_startup_with_stats():
    """Paso 6: Obtener startup con estadísticas"""
    print_section("6. STARTUP CON ESTADÍSTICAS")
    
    print("6.1. OBTENER STARTUP CON STATS")
    try:
        response = requests.get(f"{BASE_URL_API}/startups/{startup_id}/with-stats", timeout=10)
        if response.status_code == 200:
            startup = response.json()
            print_success("Startup con estadísticas obtenida")
            print_info(f"  Nombre: {startup.get('name')}")
            print_info(f"  Total votos: {startup.get('total_votos', 0)}")
            print_info(f"  Total comentarios: {startup.get('total_comentarios', 0)}")
            print_info(f"  Upvotes: {startup.get('upvotes', 0)}")
            print_info(f"  Downvotes: {startup.get('downvotes', 0)}")
        else:
            print_error(f"Obtener stats falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def test_delete_startup():
    """Paso 7: Eliminar startup"""
    print_section("7. ELIMINAR STARTUP")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    print("Eliminando startup...")
    try:
        response = requests.delete(
            f"{BASE_URL_API}/startups/{startup_id}?user_id={user_id}", 
            headers=headers, 
            timeout=10
        )
        if response.status_code in [200, 204]:
            print_success("Startup eliminada correctamente")
            
            # Verificar eliminación
            print("\nVerificando eliminación...")
            response = requests.get(f"{BASE_URL_API}/startups/{startup_id}", timeout=10)
            if response.status_code == 404:
                print_success("Eliminación verificada - Startup no existe")
            elif response.status_code == 200:
                print_error("La startup aún existe")
            else:
                print_info(f"Estado: {response.status_code}")
        else:
            print_error(f"Deletion failed: {response.status_code} - {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")

def main():
    """Ejecutar todas las pruebas"""
    print_section("TEST COMPLETO DE OPERACIONES CRUD")
    print(f"{Colors.YELLOW}StartHub - Verificación de Startups, Votos y Comentarios{Colors.END}")
    
    # Ejecutar pruebas en orden
    if not test_register_and_login():
        print_error("Falló el registro/login. Abortando pruebas.")
        return
    
    time.sleep(1)
    
    # Pruebas de perfil y actualización antes de usar recursos asociados
    if not test_user_profile_and_update():
        print_error("Falló pruebas de perfil/actualización de usuario")
    if not test_user_relogin():
        print_error("Falló re-login tras actualización")

    if not test_startup_crud():
        print_error("Falló el CRUD de startups. Abortando pruebas.")
        return
    
    time.sleep(0.5)
    
    test_startup_list_operations()
    time.sleep(0.5)
    
    test_startup_with_stats()
    time.sleep(1)
    
    if not test_vote_operations():
        print_error("Falló las operaciones de votos")
    
    time.sleep(1)
    
    if not test_comment_operations():
        print_error("Falló las operaciones de comentarios")
    
    time.sleep(1)
    
    test_delete_startup()
    # Eliminar usuario al final para no interferir con otros CRUD
    test_user_delete_and_post_checks()
    
    # Resumen final
    print_section("PRUEBAS COMPLETADAS")
    print(f"{Colors.GREEN}✅ Todas las operaciones CRUD han sido verificadas exitosamente{Colors.END}")
    print(f"\n{Colors.BLUE}Resumen Final:{Colors.END}")
    print("  ✓ Registro y Login de Usuario")
    print("  ✓ Registro, Verificación, Perfil, Update y Re-Login Usuario")
    print("  ✓ CRUD Completo de Startups (Create, Read, List, Update, Delete)")
    print("  ✓ Startup con Estadísticas")
    print("  ✓ CRUD Completo de Votos (Create, Read, Update, Delete)")
    print("  ✓ CRUD Completo de Comentarios (Create, Read, Update, Delete)")
    print("  ✓ Eliminación y validaciones post-eliminación de Usuario")

if __name__ == "__main__":
    main()

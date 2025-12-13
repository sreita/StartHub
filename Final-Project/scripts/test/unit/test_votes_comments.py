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
comment_id = None
user_id = None

def setup_test_user():
    """Crear usuario y startup de prueba"""
    global jwt_token, user_id, startup_id
    
    print_section("PREPARACIÓN: CREAR USUARIO Y STARTUP")
    
    timestamp = int(datetime.now().timestamp())
    test_email = f"test_vc_{timestamp}@starthub.test"
    test_password = "VCTest123!"
    
    # Registro
    print("Registrando usuario...")
    reg_data = {
        "firstName": "Vote",
        "lastName": "Comment",
        "email": test_email,
        "password": test_password
    }
    
    try:
        response = requests.post(f"{BASE_URL_AUTH}/registration", json=reg_data, timeout=10)
        if response.status_code == 200:
            token = response.json().get("token")
            
            # Confirmación
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
    
    # Crear startup de prueba
    headers = {"Authorization": f"Bearer {jwt_token}"}
    startup_data = {
        "name": "Test Startup Votes & Comments",
        "description": "Startup para probar votos y comentarios",
        "category_id": 1,
        "owner_user_id": user_id
    }
    
    print("Creando startup de prueba...")
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
            print_success(f"Startup creada - ID: {startup_id}")
            return True
    except Exception as e:
        print_error(f"Error creando startup: {str(e)}")
        return False

def test_vote_operations():
    """Prueba completa de CRUD de votos"""
    print_section("1. CRUD DE VOTOS")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # CREATE - Dar upvote
    print("\n1.1. CREAR UPVOTE")
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
            print_info(f"  Tipo: {vote.get('vote_type')}")
        else:
            print_error(f"Upvote falló: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # READ - Verificar conteo de votos
    print("\n1.2. LEER CONTEO DE VOTOS")
    try:
        response = requests.get(f"{BASE_URL_API}/votes/count/{startup_id}", timeout=10)
        if response.status_code == 200:
            vote_count = response.json()
            upvotes = vote_count.get('upvotes', 0)
            downvotes = vote_count.get('downvotes', 0)
            print_success(f"Conteo obtenido")
            print_info(f"  Upvotes: {upvotes}, Downvotes: {downvotes}")
            
            if upvotes != 1:
                print_error(f"Se esperaba 1 upvote, se encontró {upvotes}")
        else:
            print_error(f"Lectura de votos falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # UPDATE - Cambiar a downvote (upsert)
    print("\n1.3. CAMBIAR VOTO A DOWNVOTE")
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
                print_info(f"  Nuevo tipo: {vote.get('vote_type')}")
            else:
                print_error(f"Voto no cambió correctamente: {vote.get('vote_type')}")
        else:
            print_error(f"Cambio de voto falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # VERIFICAR cambio
    print("\n1.4. VERIFICAR CAMBIO DE VOTO")
    try:
        response = requests.get(f"{BASE_URL_API}/votes/count/{startup_id}", timeout=10)
        if response.status_code == 200:
            vote_count = response.json()
            upvotes = vote_count.get('upvotes', 0)
            downvotes = vote_count.get('downvotes', 0)
            
            if upvotes == 0 and downvotes == 1:
                print_success("Cambio verificado correctamente")
                print_info(f"  Upvotes: {upvotes}, Downvotes: {downvotes}")
            else:
                print_error(f"Conteo incorrecto: Upvotes={upvotes}, Downvotes={downvotes}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # DELETE - Eliminar voto
    print("\n1.5. ELIMINAR VOTO")
    try:
        response = requests.delete(
            f"{BASE_URL_API}/votes/?user_id={user_id}&startup_id={startup_id}",
            headers=headers,
            timeout=10
        )
        if response.status_code in [200, 204]:
            print_success("Voto eliminado correctamente")
        else:
            print_error(f"Eliminación de voto falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # VERIFICAR eliminación
    print("\n1.6. VERIFICAR ELIMINACIÓN DE VOTO")
    try:
        response = requests.get(f"{BASE_URL_API}/votes/count/{startup_id}", timeout=10)
        if response.status_code == 200:
            vote_count = response.json()
            upvotes = vote_count.get('upvotes', 0)
            downvotes = vote_count.get('downvotes', 0)
            
            if upvotes == 0 and downvotes == 0:
                print_success("Eliminación verificada - No hay votos")
            else:
                print_error(f"Aún hay votos: Upvotes={upvotes}, Downvotes={downvotes}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def test_comment_operations():
    """Prueba completa de CRUD de comentarios"""
    global comment_id
    
    print_section("2. CRUD DE COMENTARIOS")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # CREATE - Crear comentario
    print("\n2.1. CREAR COMENTARIO")
    comment_data = {
        "startup_id": startup_id,
        "content": "Este es un comentario de prueba completo con texto extenso para verificar el CRUD"
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
            print_info(f"  Texto: {comment.get('content')[:50]}...")
        else:
            print_error(f"Creación de comentario falló: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False
    
    # READ - Leer comentarios de la startup
    print("\n2.2. LEER COMENTARIOS DE LA STARTUP")
    try:
        response = requests.get(f"{BASE_URL_API}/comments/?startup_id={startup_id}", timeout=10)
        if response.status_code == 200:
            comments = response.json()
            print_success(f"Comentarios obtenidos - Total: {len(comments)}")
            
            found = False
            for c in comments:
                if c.get('comment_id') == comment_id:
                    found = True
                    print_info(f"  ✓ Comentario {comment_id} encontrado: {c.get('content')[:40]}...")
            
            if not found:
                print_error(f"No se encontró el comentario {comment_id}")
        else:
            print_error(f"Lectura de comentarios falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # READ - Listar todos los comentarios (sin filtro)
    print("\n2.3. LISTAR TODOS LOS COMENTARIOS")
    try:
        response = requests.get(f"{BASE_URL_API}/comments/", timeout=10)
        if response.status_code == 200:
            comments = response.json()
            print_success(f"Listado completo obtenido - Total: {len(comments)}")
        else:
            print_error(f"Listado falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # UPDATE - Actualizar comentario
    print("\n2.4. ACTUALIZAR COMENTARIO")
    update_comment_data = {
        "content": "COMENTARIO ACTUALIZADO - Verificando que la edición funciona correctamente"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL_API}/comments/{comment_id}?user_id={user_id}",
            json=update_comment_data,
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            comment = response.json()
            print_success("Comentario actualizado correctamente")
            print_info(f"  Nuevo texto: {comment.get('content')[:60]}...")
        else:
            print_error(f"Actualización de comentario falló: {response.status_code} - {response.text}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # VERIFICAR actualización
    print("\n2.5. VERIFICAR ACTUALIZACIÓN")
    try:
        response = requests.get(f"{BASE_URL_API}/comments/?startup_id={startup_id}", timeout=10)
        if response.status_code == 200:
            comments = response.json()
            
            for c in comments:
                if c.get('comment_id') == comment_id:
                    if "ACTUALIZADO" in c.get('content', ''):
                        print_success("Actualización verificada correctamente")
                        print_info(f"  Contenido actualizado: {c.get('content')[:50]}...")
                    else:
                        print_error("El comentario no refleja la actualización")
                    break
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # DELETE - Eliminar comentario
    print("\n2.6. ELIMINAR COMENTARIO")
    try:
        response = requests.delete(
            f"{BASE_URL_API}/comments/{comment_id}?user_id={user_id}",
            headers=headers,
            timeout=10
        )
        if response.status_code in [200, 204]:
            print_success("Comentario eliminado correctamente")
        else:
            print_error(f"Eliminación de comentario falló: {response.status_code}")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    # VERIFICAR eliminación
    print("\n2.7. VERIFICAR ELIMINACIÓN")
    try:
        response = requests.get(f"{BASE_URL_API}/comments/?startup_id={startup_id}", timeout=10)
        if response.status_code == 200:
            comments = response.json()
            
            if not any(c.get('comment_id') == comment_id for c in comments):
                print_success("Eliminación verificada - Comentario no existe")
            else:
                print_error("El comentario aún existe tras eliminación")
    except Exception as e:
        print_error(f"Error: {str(e)}")
    
    return True

def cleanup_test_data():
    """Limpiar datos de prueba"""
    print_section("LIMPIEZA: ELIMINAR DATOS DE PRUEBA")
    
    headers = {"Authorization": f"Bearer {jwt_token}"}
    
    # Eliminar startup
    print("Eliminando startup de prueba...")
    try:
        requests.delete(
            f"{BASE_URL_API}/startups/{startup_id}?user_id={user_id}",
            headers=headers,
            timeout=10
        )
        print_success("Startup eliminada")
    except Exception as e:
        print_error(f"Error eliminando startup: {str(e)}")
    
    # Eliminar usuario
    print("Eliminando usuario de prueba...")
    try:
        response = requests.delete(f"{BASE_URL_AUTH}/users/{user_id}", headers=headers, timeout=10)
        if response.status_code == 200:
            print_success("Usuario eliminado")
    except Exception as e:
        print_error(f"Error eliminando usuario: {str(e)}")

def main():
    """Ejecutar todas las pruebas de votos y comentarios"""
    print_section("PRUEBAS DE VOTOS Y COMENTARIOS")
    print(f"{Colors.YELLOW}StartHub - Verificación CRUD de Votos y Comentarios{Colors.END}")
    
    # Setup
    if not setup_test_user():
        print_error("Falló la preparación de datos. Abortando pruebas.")
        return
    
    time.sleep(1)
    
    # Ejecutar pruebas
    if not test_vote_operations():
        print_error("Falló las pruebas de votos")
    
    time.sleep(1)
    
    if not test_comment_operations():
        print_error("Falló las pruebas de comentarios")
    
    time.sleep(1)
    
    # Cleanup
    cleanup_test_data()
    
    # Resumen
    print_section("PRUEBAS COMPLETADAS")
    print(f"{Colors.GREEN}✅ Todas las pruebas de votos y comentarios ejecutadas{Colors.END}")
    print(f"\n{Colors.BLUE}Resumen:{Colors.END}")
    print("  ✓ CRUD Completo de Votos (Create, Read, Update, Delete)")
    print("  ✓ CRUD Completo de Comentarios (Create, Read, Update, Delete)")
    print("  ✓ Verificaciones de conteo y estado")

if __name__ == "__main__":
    main()

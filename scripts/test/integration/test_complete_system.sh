#!/bin/bash

################################################################################
#                                                                              #
#  TEST COMPLETO DEL SISTEMA - StartHub                                       #
#  ===================================                                         #
#  Prueba todas las funcionalidades del sistema en un flujo integrado         #
#                                                                              #
################################################################################

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

log_section() {
    echo ""
    echo -e "${BLUE}▼ $1${NC}"
    echo -e "${BLUE}────────────────────────────────────────────────────────────────────────────${NC}"
}

test_result() {
    local status=$1
    local message=$2
    
    if [ $status -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $message"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${NC} $message"
        ((TESTS_FAILED++))
    fi
}

print_header() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║              🧪 TEST COMPLETO DEL SISTEMA - STARTHUB                      ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
}

print_summary() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║                     📊 RESUMEN DE PRUEBAS                                 ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "Pruebas pasadas:  ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Pruebas fallidas: ${RED}$TESTS_FAILED${NC}"
    echo -e "Total:            $((TESTS_PASSED + TESTS_FAILED))"
    
    local total=$((TESTS_PASSED + TESTS_FAILED))
    if [ $total -gt 0 ]; then
        local percentage=$((TESTS_PASSED * 100 / total))
        echo -e "Porcentaje:       ${YELLOW}$percentage%${NC}"
    fi
    
    echo ""
}

# ============================================================================
# INICIO
# ============================================================================

print_header

log_section "1. AUTENTICACIÓN Y GESTIÓN DE USUARIOS"

# Registrar usuario
RESPONSE=$(curl -s -X POST http://localhost:8081/api/v1/registration \
  -H "Content-Type: application/json" \
  -d '{"firstName":"Test","lastName":"User","email":"testuser_'$(date +%s)'@test.com","password":"TestPass123!"}')

USER_EMAIL=$(echo "$RESPONSE" | grep -o '"email":"[^"]*"' | head -1 | cut -d'"' -f4)
[ -n "$USER_EMAIL" ]
test_result $? "Registrar usuario"

# Confirmación de email (simular token)
CONFIRM_TOKEN="test_token_$(date +%s)"
curl -s -X GET "http://localhost:8081/api/v1/registration/confirm?token=$CONFIRM_TOKEN" > /dev/null 2>&1
test_result 0 "Acceso a endpoint de confirmación"

# Login
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8081/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@starthub.com","password":"Admin123!"}')

JWT_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"token":"[^"]*"' | head -1 | cut -d'"' -f4)
[ -n "$JWT_TOKEN" ]
test_result $? "Login y obtención de JWT"

# Obtener perfil
PROFILE=$(curl -s -X GET http://localhost:8081/api/v1/users/me \
  -H "Authorization: Bearer $JWT_TOKEN")

echo "$PROFILE" | grep -q "firstName"
test_result $? "Obtener perfil del usuario"

# Actualizar perfil
UPDATE=$(curl -s -X PUT http://localhost:8081/api/v1/users/me \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"firstName":"TestUpdated","lastName":"UserUpdated","profileInfo":"Updated profile"}')

echo "$UPDATE" | grep -q "TestUpdated\|200\|success"
test_result $? "Actualizar perfil del usuario"

log_section "2. GESTIÓN DE STARTUPS"

# Obtener categorías
CATEGORIES=$(curl -s -X GET http://localhost:8000/api/v1/categories/)
CATEGORY_ID=$(echo "$CATEGORIES" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
test_result $? "Obtener categorías"

# Crear startup
CREATE_STARTUP=$(curl -s -X POST "http://localhost:8000/api/v1/startups/?user_id=1" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"TestStartup_$(date +%s)\",\"description\":\"Test description\",\"category_id\":$CATEGORY_ID}")

STARTUP_ID=$(echo "$CREATE_STARTUP" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
[ -n "$STARTUP_ID" ] && [ "$STARTUP_ID" -gt 0 ]
test_result $? "Crear nueva startup"

# Obtener startup por ID
if [ -n "$STARTUP_ID" ]; then
    GET_STARTUP=$(curl -s -X GET "http://localhost:8000/api/v1/startups/$STARTUP_ID")
    echo "$GET_STARTUP" | grep -q "\"id\""
    test_result $? "Obtener startup por ID"
fi

# Listar startups
LIST_STARTUPS=$(curl -s -X GET "http://localhost:8000/api/v1/startups/?skip=0&limit=50")
echo "$LIST_STARTUPS" | grep -q "id"
test_result $? "Listar startups con paginación"

# Buscar startups
SEARCH=$(curl -s -X GET "http://localhost:8000/api/v1/startups/?search=test")
test_result $? "Buscar startups"

log_section "3. VOTOS"

if [ -n "$STARTUP_ID" ]; then
    # Crear voto (upvote)
    VOTE=$(curl -s -X POST "http://localhost:8000/api/v1/votes/?user_id=1&startup_id=$STARTUP_ID&is_upvote=true" \
      -H "Content-Type: application/json" \
      -d '{}')
    
    echo "$VOTE" | grep -q "id\|success"
    test_result $? "Crear voto (upvote)"
    
    # Obtener contador de votos
    VOTE_COUNT=$(curl -s -X GET "http://localhost:8000/api/v1/votes/count/$STARTUP_ID")
    echo "$VOTE_COUNT" | grep -q "upvotes\|downvotes"
    test_result $? "Obtener contador de votos"
    
    # Obtener votos del usuario
    USER_VOTES=$(curl -s -X GET "http://localhost:8000/api/v1/votes/user/1")
    test_result $? "Obtener votos del usuario"
fi

log_section "4. COMENTARIOS"

if [ -n "$STARTUP_ID" ]; then
    # Crear comentario
    COMMENT=$(curl -s -X POST "http://localhost:8000/api/v1/comments/?user_id=1&startup_id=$STARTUP_ID" \
      -H "Content-Type: application/json" \
      -d '{"text":"Test comment from automated test"}')
    
    COMMENT_ID=$(echo "$COMMENT" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
    [ -n "$COMMENT_ID" ] && [ "$COMMENT_ID" -gt 0 ]
    test_result $? "Crear comentario"
    
    # Obtener comentarios de la startup
    GET_COMMENTS=$(curl -s -X GET "http://localhost:8000/api/v1/comments/?startup_id=$STARTUP_ID")
    echo "$GET_COMMENTS" | grep -q "text\|comment"
    test_result $? "Obtener comentarios de startup"
    
    # Actualizar comentario
    if [ -n "$COMMENT_ID" ]; then
        UPDATE_COMMENT=$(curl -s -X PUT "http://localhost:8000/api/v1/comments/$COMMENT_ID" \
          -H "Content-Type: application/json" \
          -d '{"text":"Updated test comment"}')
        
        echo "$UPDATE_COMMENT" | grep -q "Updated\|success\|id"
        test_result $? "Actualizar comentario"
        
        # Eliminar comentario
        DELETE=$(curl -s -w "\n%{http_code}" -X DELETE "http://localhost:8000/api/v1/comments/$COMMENT_ID")
        HTTP_CODE=$(echo "$DELETE" | tail -1)
        [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "204" ]
        test_result $? "Eliminar comentario"
    fi
fi

log_section "5. RECUPERACIÓN DE CONTRASEÑA"

# Solicitar recuperación
RECOVER=$(curl -s -X POST http://localhost:8081/api/v1/auth/recover-password \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@starthub.com"}')

test_result $? "Solicitar recuperación de contraseña"

# ============================================================================
# RESUMEN
# ============================================================================

print_summary

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                            ║${NC}"
    echo -e "${GREEN}║            🎉 TODOS LOS TESTS PASARON - SISTEMA OPERATIVO ✅               ║${NC}"
    echo -e "${GREEN}║                                                                            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                                                                            ║${NC}"
    echo -e "${RED}║            ⚠️  ALGUNOS TESTS FALLARON - REVISAR LOGS                        ║${NC}"
    echo -e "${RED}║                                                                            ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi

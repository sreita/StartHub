#!/bin/bash

################################################################################
#                                                                              #
#  TEST DE INTERACCIONES - StartHub                                           #
#  ================================                                            #
#  Prueba votos, comentarios y otras interacciones                            #
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
    echo "║          💬 TEST DE INTERACCIONES - STARTHUB                              ║"
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

log_section "CONFIGURACIÓN: OBTENER STARTUP DE PRUEBA"

# Obtener una startup de prueba
STARTUP=$(curl -s -X GET "http://localhost:8000/api/v1/startups/?skip=0&limit=1")
STARTUP_ID=$(echo "$STARTUP" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

if [ -z "$STARTUP_ID" ]; then
    echo -e "${RED}No hay startups disponibles. Crear una primero.${NC}"
    STARTUP_ID=1
fi

echo -e "Usando startup ID: ${YELLOW}$STARTUP_ID${NC}"

log_section "VOTOS"

# 1. Crear voto (upvote)
VOTE=$(curl -s -X POST "http://localhost:8000/api/v1/votes/?user_id=1&startup_id=$STARTUP_ID&is_upvote=true" \
  -H "Content-Type: application/json" \
  -d '{}')

echo "$VOTE" | grep -q "id\|success" || test_result $? "POST /api/v1/votes/ - Crear voto (upvote)"
test_result $? "POST /api/v1/votes/ - Crear voto (upvote)"

# 2. Obtener contador de votos
VOTE_COUNT=$(curl -s -X GET "http://localhost:8000/api/v1/votes/count/$STARTUP_ID")
echo "$VOTE_COUNT" | grep -q "upvotes\|downvotes"
test_result $? "GET /api/v1/votes/count/{id} - Obtener contador de votos"

# 3. Obtener votos del usuario
USER_VOTES=$(curl -s -X GET "http://localhost:8000/api/v1/votes/user/1")
test_result $? "GET /api/v1/votes/user/{id} - Obtener votos del usuario"

log_section "COMENTARIOS"

# 4. Crear comentario
COMMENT=$(curl -s -X POST "http://localhost:8000/api/v1/comments/?user_id=1&startup_id=$STARTUP_ID" \
  -H "Content-Type: application/json" \
  -d '{"text":"Test comment from automated test"}')

COMMENT_ID=$(echo "$COMMENT" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
[ -n "$COMMENT_ID" ] && [ "$COMMENT_ID" -gt 0 ]
test_result $? "POST /api/v1/comments/ - Crear comentario"

# 5. Obtener comentarios de la startup
COMMENTS=$(curl -s -X GET "http://localhost:8000/api/v1/comments/?startup_id=$STARTUP_ID")
echo "$COMMENTS" | grep -q "text\|comment"
test_result $? "GET /api/v1/comments/ - Obtener comentarios de startup"

# 6. Actualizar comentario
if [ -n "$COMMENT_ID" ]; then
    UPDATE_COMMENT=$(curl -s -X PUT "http://localhost:8000/api/v1/comments/$COMMENT_ID" \
      -H "Content-Type: application/json" \
      -d '{"text":"Updated test comment"}')
    
    echo "$UPDATE_COMMENT" | grep -q "Updated\|success\|id"
    test_result $? "PUT /api/v1/comments/{id} - Actualizar comentario"
else
    echo -e "${RED}✗${NC} PUT /api/v1/comments/{id} - Actualizar comentario (sin ID)"
    ((TESTS_FAILED++))
fi

# 7. Eliminar comentario
if [ -n "$COMMENT_ID" ]; then
    DELETE=$(curl -s -w "\n%{http_code}" -X DELETE "http://localhost:8000/api/v1/comments/$COMMENT_ID")
    HTTP_CODE=$(echo "$DELETE" | tail -1)
    [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "204" ]
    test_result $? "DELETE /api/v1/comments/{id} - Eliminar comentario"
else
    echo -e "${RED}✗${NC} DELETE /api/v1/comments/{id} - Eliminar comentario (sin ID)"
    ((TESTS_FAILED++))
fi

# ============================================================================
# RESUMEN
# ============================================================================

print_summary

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                            ║${NC}"
    echo -e "${GREEN}║            ✅ INTERACCIONES COMPLETAMENTE FUNCIONALES                      ║${NC}"
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

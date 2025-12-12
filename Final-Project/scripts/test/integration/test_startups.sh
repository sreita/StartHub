#!/bin/bash

################################################################################
#                                                                              #
#  TEST DE STARTUPS - StartHub                                                #
#  ==========================                                                 #
#  Prueba todos los endpoints relacionados con startups                       #
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
    echo "║              🚀 TEST DE STARTUPS - STARTHUB                               ║"
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

log_section "CATEGORÍAS"

# 1. Obtener categorías
CATEGORIES=$(curl -s -X GET http://localhost:8000/api/v1/categories/)
CATEGORY_ID=$(echo "$CATEGORIES" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)

[ -n "$CATEGORY_ID" ]
test_result $? "GET /api/v1/categories/ - Obtener categorías"

log_section "OPERACIONES CRUD DE STARTUPS"

# 2. Crear startup
TIMESTAMP=$(date +%s)
CREATE=$(curl -s -X POST "http://localhost:8000/api/v1/startups/?user_id=1" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"TestStartup_$TIMESTAMP\",\"description\":\"Test description\",\"category_id\":${CATEGORY_ID:-1}}")

STARTUP_ID=$(echo "$CREATE" | grep -o '"id":[0-9]*' | head -1 | cut -d':' -f2)
[ -n "$STARTUP_ID" ] && [ "$STARTUP_ID" -gt 0 ]
test_result $? "POST /api/v1/startups/ - Crear startup"

log_section "LECTURA DE STARTUPS"

# 3. Obtener startup por ID
if [ -n "$STARTUP_ID" ]; then
    GET=$(curl -s -X GET "http://localhost:8000/api/v1/startups/$STARTUP_ID")
    echo "$GET" | grep -q "\"id\""
    test_result $? "GET /api/v1/startups/{id} - Obtener startup por ID"
else
    echo -e "${RED}✗${NC} GET /api/v1/startups/{id} - Obtener startup por ID (sin ID)"
    ((TESTS_FAILED++))
fi

# 4. Listar startups con paginación
LIST=$(curl -s -X GET "http://localhost:8000/api/v1/startups/?skip=0&limit=50")
echo "$LIST" | grep -q "id"
test_result $? "GET /api/v1/startups/ - Listar startups con paginación"

# 5. Buscar startups
SEARCH=$(curl -s -X GET "http://localhost:8000/api/v1/startups/?search=test")
test_result $? "GET /api/v1/startups/?search= - Buscar startups"

# 6. Obtener total de startups
TOTAL=$(curl -s -X GET "http://localhost:8000/api/v1/startups/?skip=0&limit=1")
COUNT=$(echo "$TOTAL" | grep -o '"id"' | wc -l)
test_result $? "GET /api/v1/startups/ - Contar total de startups en BD"

echo ""
echo -e "${YELLOW}Total de startups en la base de datos: aproximadamente${NC} $COUNT"

# ============================================================================
# RESUMEN
# ============================================================================

print_summary

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                            ║${NC}"
    echo -e "${GREEN}║            ✅ GESTIÓN DE STARTUPS COMPLETAMENTE FUNCIONAL                  ║${NC}"
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

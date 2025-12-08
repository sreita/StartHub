#!/bin/bash

################################################################################
#                                                                              #
#  TEST E2E DOCKER - StartHub                                                 #
#  ===========================                                                 #
#  Ejecuta todos los tests en contenedores Docker                             #
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
    echo "║              🐳 TEST E2E DOCKER - STARTHUB                                ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
}

print_summary() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║                     📊 RESUMEN DE PRUEBAS E2E                             ║"
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

log_section "VERIFICACIÓN DE CONTENEDORES DOCKER"

# Verificar que Docker está corriendo
if ! docker ps &> /dev/null; then
    echo -e "${RED}❌ Error: Docker no está corriendo${NC}"
    exit 1
fi

test_result $? "Docker está disponible"

# Verificar contenedores
COMPOSE_FILE="${1:-../../docker/compose.yaml}"

if [ ! -f "$COMPOSE_FILE" ]; then
    echo -e "${YELLOW}⚠️  Archivo compose no encontrado: $COMPOSE_FILE${NC}"
    COMPOSE_FILE="docker/compose.yaml"
fi

# Verificar Spring Boot
if docker ps | grep -q "starthub-spring"; then
    test_result 0 "Contenedor Spring Boot (8081) en ejecución"
else
    echo -e "${RED}✗${NC} Contenedor Spring Boot (8081) no encontrado"
    ((TESTS_FAILED++))
fi

# Verificar FastAPI
if docker ps | grep -q "starthub-fastapi"; then
    test_result 0 "Contenedor FastAPI (8000) en ejecución"
else
    echo -e "${RED}✗${NC} Contenedor FastAPI (8000) no encontrado"
    ((TESTS_FAILED++))
fi

# Verificar MySQL
if docker ps | grep -q "starthub-db"; then
    test_result 0 "Contenedor MySQL en ejecución"
else
    echo -e "${RED}✗${NC} Contenedor MySQL no encontrado"
    ((TESTS_FAILED++))
fi

log_section "VERIFICACIÓN DE CONECTIVIDAD"

# Spring Boot
if curl -s http://localhost:8081/api/v1/auth/login -X OPTIONS &> /dev/null; then
    test_result 0 "Spring Boot responde en puerto 8081"
else
    echo -e "${RED}✗${NC} Spring Boot no responde en puerto 8081"
    ((TESTS_FAILED++))
fi

# FastAPI
if curl -s http://localhost:8000/api/v1/categories/ &> /dev/null; then
    test_result 0 "FastAPI responde en puerto 8000"
else
    echo -e "${RED}✗${NC} FastAPI no responde en puerto 8000"
    ((TESTS_FAILED++))
fi

# MySQL
if docker exec starthub-db mysql -u root -proot starthub_db -e "SELECT 1" &> /dev/null; then
    test_result 0 "Base de datos MySQL accesible"
else
    echo -e "${RED}✗${NC} Base de datos MySQL no accesible"
    ((TESTS_FAILED++))
fi

log_section "EJECUCIÓN DE TESTS DE INTEGRACIÓN"

# Tests de autenticación
if bash ../test/integration/test_authentication.sh > /dev/null 2>&1; then
    test_result 0 "Tests de autenticación"
else
    test_result 1 "Tests de autenticación"
fi

# Tests de startups
if bash ../test/integration/test_startups.sh > /dev/null 2>&1; then
    test_result 0 "Tests de startups"
else
    test_result 1 "Tests de startups"
fi

# Tests de interacciones
if bash ../test/integration/test_interactions.sh > /dev/null 2>&1; then
    test_result 0 "Tests de interacciones"
else
    test_result 1 "Tests de interacciones"
fi

# ============================================================================
# RESUMEN
# ============================================================================

print_summary

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                            ║${NC}"
    echo -e "${GREEN}║            ✅ TODOS LOS TESTS E2E PASARON - SISTEMA OPERATIVO              ║${NC}"
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

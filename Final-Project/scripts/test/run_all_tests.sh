#!/bin/bash

################################################################################
#                                                                              #
#  TEST MAESTRO - StartHub                                                    #
#  ==========================                                                 #
#  Ejecuta todos los tests del sistema y genera un reporte                    #
#                                                                              #
################################################################################

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colores para salida
print_header() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║                  🧪 TEST MAESTRO - STARTHUB                               ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    echo ""
}

print_test() {
    echo -e "${BLUE}────────────────────────────────────────────────────────────────────────────${NC}"
    echo -e "${YELLOW}Ejecutando: $1${NC}"
    echo -e "${BLUE}────────────────────────────────────────────────────────────────────────────${NC}"
}

# Verificar que Docker está corriendo
check_docker() {
    if ! docker ps &> /dev/null; then
        echo -e "${RED}❌ Error: Docker no está corriendo${NC}"
        exit 1
    fi
}

# Verificar conectividad
check_connectivity() {
    echo ""
    echo "Verificando conectividad..."
    
    # Spring Boot
    if ! curl -s http://localhost:8081/api/v1/auth/login -X OPTIONS &> /dev/null; then
        echo -e "${RED}⚠️  Spring Boot (8081) no responde${NC}"
        return 1
    else
        echo -e "${GREEN}✓${NC} Spring Boot (8081) disponible"
    fi
    
    # FastAPI
    if ! curl -s http://localhost:8000/api/v1/categories/ &> /dev/null; then
        echo -e "${RED}⚠️  FastAPI (8000) no responde${NC}"
        return 1
    else
        echo -e "${GREEN}✓${NC} FastAPI (8000) disponible"
    fi
    
    # Base de datos
    if ! docker exec starthub-db mysql -u root -proot starthub_db -e "SELECT 1" &> /dev/null; then
        echo -e "${RED}⚠️  Base de datos no disponible${NC}"
        return 1
    else
        echo -e "${GREEN}✓${NC} Base de datos disponible"
    fi
    
    return 0
}

# ============================================================================
# INICIO
# ============================================================================

print_header

check_docker

if ! check_connectivity; then
    echo ""
    echo -e "${RED}Error: No se pudo conectar a los servicios${NC}"
    echo "Asegúrate de que todos los contenedores están corriendo:"
    echo "  docker compose -f docker/compose.yaml up -d"
    exit 1
fi

TOTAL_PASS=0
TOTAL_FAIL=0
RESULTS=()

# ============================================================================
# EJECUTAR TESTS
# ============================================================================

echo ""
echo -e "${YELLOW}Iniciando suite de tests...${NC}"
echo ""

# Test de autenticación
print_test "Test de Autenticación"
if bash "$SCRIPT_DIR/test_authentication.sh" 2>&1; then
    RESULTS+=("${GREEN}✓${NC} Autenticación")
    ((TOTAL_PASS++))
else
    RESULTS+=("${RED}✗${NC} Autenticación")
    ((TOTAL_FAIL++))
fi

# Test de startups
print_test "Test de Startups"
if bash "$SCRIPT_DIR/test_startups.sh" 2>&1; then
    RESULTS+=("${GREEN}✓${NC} Startups")
    ((TOTAL_PASS++))
else
    RESULTS+=("${RED}✗${NC} Startups")
    ((TOTAL_FAIL++))
fi

# Test de interacciones
print_test "Test de Interacciones (Votos y Comentarios)"
if bash "$SCRIPT_DIR/test_interactions.sh" 2>&1; then
    RESULTS+=("${GREEN}✓${NC} Interacciones")
    ((TOTAL_PASS++))
else
    RESULTS+=("${RED}✗${NC} Interacciones")
    ((TOTAL_FAIL++))
fi

# Test completo del sistema
print_test "Test Completo del Sistema"
if bash "$SCRIPT_DIR/test_complete_system.sh" 2>&1; then
    RESULTS+=("${GREEN}✓${NC} Sistema Completo")
    ((TOTAL_PASS++))
else
    RESULTS+=("${RED}✗${NC} Sistema Completo")
    ((TOTAL_FAIL++))
fi

# ============================================================================
# REPORTE FINAL
# ============================================================================

echo ""
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║                  📊 REPORTE FINAL DE TESTS                                ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "Resultados de las suites de test:"
echo ""
for result in "${RESULTS[@]}"; do
    echo -e "  $result"
done

echo ""
echo "════════════════════════════════════════════════════════════════════════════="
echo ""
echo -e "Suites Pasadas:  ${GREEN}$TOTAL_PASS${NC}"
echo -e "Suites Fallidas: ${RED}$TOTAL_FAIL${NC}"
echo -e "Total Suites:    $((TOTAL_PASS + TOTAL_FAIL))"

if [ $TOTAL_FAIL -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║            🎉 TODOS LOS TESTS PASARON - SISTEMA OPERATIVO ✅              ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║            ⚠️  ALGUNOS TESTS FALLARON - REVISAR LOGS                      ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    exit 1
fi

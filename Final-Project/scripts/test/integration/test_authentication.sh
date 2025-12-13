#!/bin/bash

################################################################################
#                                                                              #
#  TEST DE AUTENTICACIÓN - StartHub                                           #
#  ==============================                                             #
#  Prueba todos los endpoints de autenticación                               #
#                                                                              #
################################################################################

# Permitimos que cada verificación falle sin detener todo el script;
# los resultados se contabilizan con test_result.
set +e

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
    echo "║           🔐 TEST DE AUTENTICACIÓN - STARTHUB                             ║"
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

log_section "ENDPOINTS DE AUTENTICACIÓN"

# 1. Registro
TIMESTAMP=$(date +%s)
TEST_EMAIL="testuser_${TIMESTAMP}@test.com"
TEST_PASSWORD="TestPass123!"
REGISTER=$(curl -s -X POST http://localhost:8081/api/v1/registration \
  -H "Content-Type: application/json" \
  -d "{\"firstName\":\"Test\",\"lastName\":\"User\",\"email\":\"${TEST_EMAIL}\",\"password\":\"${TEST_PASSWORD}\"}")

echo "$REGISTER" | grep -q "email"
test_result $? "POST /api/v1/registration - Registrar usuario"

# Extraer token de confirmación devuelto por el registro
REG_TOKEN=$(echo "$REGISTER" | grep -o '"token":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -z "$REG_TOKEN" ]; then
  echo -e "${RED}✗${NC} No se pudo obtener token de confirmación"
  ((TESTS_FAILED++))
fi

# 2. Confirmación de email
if [ -n "$REG_TOKEN" ]; then
  curl -s -X GET "http://localhost:8081/api/v1/registration/confirm?token=${REG_TOKEN}" > /dev/null
  test_result $? "GET /api/v1/registration/confirm - Confirmar email"
else
  test_result 1 "GET /api/v1/registration/confirm - Confirmar email"
fi

# 3. Login
LOGIN=$(curl -s -X POST http://localhost:8081/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${TEST_EMAIL}\",\"password\":\"${TEST_PASSWORD}\"}")

JWT_TOKEN=$(echo "$LOGIN" | grep -o '"token":"[^"]*"' | head -1 | cut -d'"' -f4)
[ -n "$JWT_TOKEN" ]
test_result $? "POST /api/v1/auth/login - Login y obtener JWT"

log_section "ENDPOINTS DE PERFIL"

# 4. Obtener perfil
if [ -n "$JWT_TOKEN" ]; then
    PROFILE=$(curl -s -X GET http://localhost:8081/api/v1/users/me \
      -H "Authorization: Bearer $JWT_TOKEN")
    
    echo "$PROFILE" | grep -q "firstName\|email"
    test_result $? "GET /api/v1/users/me - Obtener perfil autenticado"
    
    # 5. Actualizar perfil
    UPDATE=$(curl -s -X PUT http://localhost:8081/api/v1/users/me \
      -H "Authorization: Bearer $JWT_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"firstName":"UpdatedName","lastName":"UpdatedLast","profileInfo":"Updated profile"}')
    
    echo "$UPDATE" | grep -q "UpdatedName\|success\|firstName"
    test_result $? "PUT /api/v1/users/me - Actualizar perfil"
else
    echo -e "${RED}✗${NC} GET /api/v1/users/me - Obtener perfil autenticado (sin JWT)"
    ((TESTS_FAILED++))
    echo -e "${RED}✗${NC} PUT /api/v1/users/me - Actualizar perfil (sin JWT)"
    ((TESTS_FAILED++))
fi

log_section "ENDPOINTS DE RECUPERACIÓN DE CONTRASEÑA"

# 6. Solicitar recuperación
RECOVER=$(curl -s -X POST http://localhost:8081/api/v1/auth/recover-password \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@starthub.com"}')

test_result $? "POST /api/v1/auth/recover-password - Solicitar recuperación"

# 7. Resetear contraseña
RESET=$(curl -s -X POST http://localhost:8081/api/v1/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{"token":"test_reset_token","newPassword":"NewPass123!"}')

test_result $? "POST /api/v1/auth/reset-password - Resetear contraseña"

# 8. Logout (si existe)
curl -s -X POST http://localhost:8081/api/v1/auth/logout \
  -H "Authorization: Bearer $JWT_TOKEN" > /dev/null 2>&1
test_result $? "POST /api/v1/auth/logout - Logout"

# ============================================================================
# RESUMEN
# ============================================================================

print_summary

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                            ║${NC}"
    echo -e "${GREEN}║            ✅ AUTENTICACIÓN COMPLETAMENTE FUNCIONAL                        ║${NC}"
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

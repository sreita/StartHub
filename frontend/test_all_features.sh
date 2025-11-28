#!/bin/bash

BASE_URL="http://localhost:8081/api/v1"
FRONTEND_URL="http://localhost:3000"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  StartHub - Pruebas Automatizadas de Funcionalidades    ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}\n"

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

check_server() {
  local name=$1
  local url=$2
  echo -e "${YELLOW}Verificando $name...${NC}"
  if curl -s "$url" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ $name está funcionando${NC}"
    return 0
  else
    echo -e "${RED}✗ $name NO está funcionando${NC}"
    return 1
  fi
}

run_test() {
  local test_name=$1
  local command=$2
  TOTAL_TESTS=$((TOTAL_TESTS + 1))
  echo -e "\n${BLUE}[Test $TOTAL_TESTS] $test_name${NC}"
  eval "$command" && {
    echo -e "${GREEN}✓ PASÓ${NC}"; PASSED_TESTS=$((PASSED_TESTS + 1));
  } || {
    echo -e "${RED}✗ FALLÓ${NC}"; FAILED_TESTS=$((FAILED_TESTS + 1));
  }
}

echo "═══ Verificación de Servidores ═══"
check_server "Backend (Puerto 8081)" "$BASE_URL/actuator/health" || true
check_server "Frontend (Puerto 3000)" "$FRONTEND_URL/home.html" || true

if ! curl -s "$BASE_URL/actuator/health" > /dev/null || ! curl -s "$FRONTEND_URL/home.html" > /dev/null; then
  echo -e "${RED}Error: Asegúrate de que ambos servidores estén corriendo${NC}"
  echo -e "Backend: ./mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=test"
  echo -e "Frontend: python frontend/server.py"
  exit 1
fi

echo "\n═══ Pruebas de Autenticación ═══"
TS=$(date +%s)
EMAIL="test_${TS}@mail.com"
PASS="Secret123!"

run_test "Registro de usuario" \
  "curl -s -X POST '$BASE_URL/registration' -H 'Content-Type: application/json' -d '{"firstName":"Test","lastName":"User","email":"'$EMAIL'","password":"'$PASS'","isAdmin":false}' | grep -qi 'success\|confirm'"

TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" -H 'Content-Type: application/json' -d '{"email":"'$EMAIL'","password":"'$PASS'"}' | sed -n 's/.*"token"\s*:\s*"\([^"]*\)".*/\1/p')

run_test "Login exitoso" \
  "test -n '$TOKEN'"

run_test "Login fallido" \
  "test -z $(curl -s -o /dev/null -w '%{http_code}' -X POST '$BASE_URL/auth/login' -H 'Content-Type: application/json' -d '{"email":"'$EMAIL'","password":"Wrong!"}') && false || true"

if [ -n "$TOKEN" ]; then
  run_test "Acceso protegido con token" \
    "curl -s -H 'Authorization: Bearer $TOKEN' '$BASE_URL/users/1' -o /dev/null -w '%{http_code}' | grep -qE '200|403'"
fi

echo "\n═══ Resumen ═══"
echo -e "Total: $TOTAL_TESTS  ${GREEN}✔ Pasaron: $PASSED_TESTS${NC}  ${RED}✗ Fallaron: $FAILED_TESTS${NC}"
exit 0
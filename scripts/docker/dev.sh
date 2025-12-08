#!/bin/bash

################################################################################
#                                                                              #
#  DEV.SH - Modo Desarrollo                                                   #
#  ============================                                               #
#  Inicia Docker con logs en tiempo real                                      #
#                                                                              #
################################################################################

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
COMPOSE_FILE="$PROJECT_ROOT/docker/compose.yaml"

print_header() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║                  🛠️  STARTHUB MODO DESARROLLO                             ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    echo ""
}

print_info() {
    echo -e "${BLUE}Servicios disponibles:${NC}"
    echo ""
    echo "  🌐 Frontend:        http://localhost:3000"
    echo "  🔐 Spring Boot:     http://localhost:8081"
    echo "  🐍 FastAPI:         http://localhost:8000"
    echo "  📊 MySQL:           localhost:3307"
    echo "  📧 MailHog:         http://localhost:8025"
    echo ""
    echo -e "${YELLOW}Presiona Ctrl+C para detener los contenedores${NC}"
    echo ""
}

print_header

# Verificar Docker
if ! docker --version &> /dev/null; then
    echo -e "${RED}❌ Error: Docker no está instalado${NC}"
    exit 1
fi

if ! docker ps &> /dev/null; then
    echo -e "${RED}❌ Error: Docker no está corriendo${NC}"
    exit 1
fi

if [ ! -f "$COMPOSE_FILE" ]; then
    echo -e "${RED}❌ Error: docker/compose.yaml no encontrado${NC}"
    exit 1
fi

# Iniciar contenedores
echo -e "${YELLOW}Iniciando contenedores...${NC}"
cd "$PROJECT_ROOT"
docker compose -f docker/compose.yaml up

print_info

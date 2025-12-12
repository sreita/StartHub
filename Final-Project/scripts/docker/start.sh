#!/bin/bash

################################################################################
#                                                                              #
#  START.SH - StartHub Docker Manager                                         #
#  ===================================                                         #
#  Script para iniciar/parar/gestionar el proyecto con Docker                 #
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

# Funciones de utilidad
print_header() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║                     🚀 STARTHUB DOCKER MANAGER                            ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    echo ""
}

print_menu() {
    echo "Opciones disponibles:"
    echo ""
    echo "  ${BLUE}start${NC}           - Iniciar todos los contenedores"
    echo "  ${BLUE}stop${NC}            - Detener todos los contenedores"
    echo "  ${BLUE}restart${NC}         - Reiniciar todos los contenedores"
    echo "  ${BLUE}status${NC}          - Ver estado de contenedores"
    echo "  ${BLUE}logs${NC}            - Ver logs de todos los servicios"
    echo "  ${BLUE}logs <service>${NC}  - Ver logs de un servicio específico"
    echo "  ${BLUE}build${NC}           - Construir imágenes sin cachéy"
    echo "  ${BLUE}rebuild${NC}         - Reconstruir todos los contenedores"
    echo "  ${BLUE}clean${NC}           - Limpiar volúmenes y contenedores"
    echo "  ${BLUE}test${NC}            - Ejecutar tests de integración"
    echo "  ${BLUE}shell <service>${NC} - Abrir shell en un contenedor"
    echo ""
}

check_docker() {
    if ! docker --version &> /dev/null; then
        echo -e "${RED}❌ Error: Docker no está instalado${NC}"
        exit 1
    fi
    
    if ! docker ps &> /dev/null; then
        echo -e "${RED}❌ Error: Docker no está corriendo${NC}"
        exit 1
    fi
}

check_compose_file() {
    if [ ! -f "$COMPOSE_FILE" ]; then
        echo -e "${RED}❌ Error: docker/compose.yaml no encontrado${NC}"
        exit 1
    fi
}

cmd_start() {
    echo -e "${YELLOW}Iniciando contenedores...${NC}"
    cd "$PROJECT_ROOT"
    docker compose -f docker/compose.yaml up -d
    echo -e "${GREEN}✓${NC} Contenedores iniciados"
    echo ""
    cmd_status
}

cmd_stop() {
    echo -e "${YELLOW}Deteniendo contenedores...${NC}"
    cd "$PROJECT_ROOT"
    docker compose -f docker/compose.yaml stop
    echo -e "${GREEN}✓${NC} Contenedores detenidos"
}

cmd_restart() {
    cmd_stop
    echo ""
    sleep 2
    cmd_start
}

cmd_status() {
    echo -e "${BLUE}Estado de los contenedores:${NC}"
    echo ""
    cd "$PROJECT_ROOT"
    docker compose -f docker/compose.yaml ps
}

cmd_logs() {
    cd "$PROJECT_ROOT"
    if [ -n "$1" ]; then
        echo -e "${BLUE}Logs de $1:${NC}"
        docker compose -f docker/compose.yaml logs -f "$1"
    else
        echo -e "${BLUE}Logs de todos los servicios:${NC}"
        docker compose -f docker/compose.yaml logs -f
    fi
}

cmd_build() {
    echo -e "${YELLOW}Construyendo imágenes (sin cachéy)...${NC}"
    cd "$PROJECT_ROOT"
    docker compose -f docker/compose.yaml build --no-cache
    echo -e "${GREEN}✓${NC} Imágenes construidas"
}

cmd_rebuild() {
    echo -e "${YELLOW}Reconstruyendo contenedores...${NC}"
    cmd_stop
    cmd_build
    cmd_start
}

cmd_clean() {
    echo -e "${YELLOW}Limpiando volúmenes y contenedores...${NC}"
    cd "$PROJECT_ROOT"
    docker compose -f docker/compose.yaml down -v
    echo -e "${GREEN}✓${NC} Limpieza completada"
}

cmd_test() {
    echo -e "${YELLOW}Ejecutando tests...${NC}"
    echo ""
    
    if [ ! -f "$SCRIPT_DIR/../test/integration/test_complete_system.sh" ]; then
        echo -e "${RED}❌ Error: Tests no encontrados${NC}"
        exit 1
    fi
    
    bash "$SCRIPT_DIR/../test/integration/test_complete_system.sh"
}

cmd_shell() {
    if [ -z "$1" ]; then
        echo -e "${RED}❌ Error: Especifica un servicio${NC}"
        echo "Servicios disponibles:"
        cd "$PROJECT_ROOT"
        docker compose -f docker/compose.yaml config --services
        exit 1
    fi
    
    cd "$PROJECT_ROOT"
    docker compose -f docker/compose.yaml exec "$1" /bin/bash
}

# ============================================================================
# PRINCIPAL
# ============================================================================

print_header
check_docker
check_compose_file

COMMAND="${1:-menu}"

case "$COMMAND" in
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    restart)
        cmd_restart
        ;;
    status)
        cmd_status
        ;;
    logs)
        cmd_logs "$2"
        ;;
    build)
        cmd_build
        ;;
    rebuild)
        cmd_rebuild
        ;;
    clean)
        cmd_clean
        ;;
    test)
        cmd_test
        ;;
    shell)
        cmd_shell "$2"
        ;;
    menu|help|-h|--help)
        print_menu
        ;;
    *)
        echo -e "${RED}❌ Comando desconocido: $COMMAND${NC}"
        echo ""
        print_menu
        exit 1
        ;;
esac

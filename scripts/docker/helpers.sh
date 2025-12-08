#!/bin/bash

################################################################################
#                                                                              #
#  DOCKER HELPERS - Funciones auxiliares para Docker                          #
#  =================================================                           #
#                                                                              #
################################################################################

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Obtener directorio del proyecto
get_project_root() {
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
    echo "$(cd "$script_dir/../.." && pwd)"
}

# Verificar que Docker está disponible
check_docker() {
    if ! docker --version &> /dev/null; then
        echo -e "${RED}❌ Error: Docker no está instalado${NC}"
        return 1
    fi
    
    if ! docker ps &> /dev/null; then
        echo -e "${RED}❌ Error: Docker no está corriendo${NC}"
        return 1
    fi
    
    return 0
}

# Obtener el archivo compose correcto
get_compose_file() {
    local project_root="$(get_project_root)"
    local compose_file="$project_root/docker/compose.yaml"
    
    if [ ! -f "$compose_file" ]; then
        echo -e "${RED}❌ Error: docker/compose.yaml no encontrado${NC}"
        return 1
    fi
    
    echo "$compose_file"
}

# Esperar a que un servicio esté listo
wait_for_service() {
    local service=$1
    local port=$2
    local max_attempts=30
    local attempt=0
    
    echo -e "${YELLOW}Esperando a que $service esté listo...${NC}"
    
    while [ $attempt -lt $max_attempts ]; do
        if nc -z localhost $port 2>/dev/null; then
            echo -e "${GREEN}✓${NC} $service está listo"
            return 0
        fi
        
        ((attempt++))
        sleep 1
    done
    
    echo -e "${RED}✗${NC} $service no responde después de ${max_attempts}s"
    return 1
}

# Ejecutar comando en contenedor
docker_exec() {
    local service=$1
    shift
    local project_root="$(get_project_root)"
    
    cd "$project_root"
    docker compose -f docker/compose.yaml exec "$service" "$@"
}

# Ver logs de servicio
docker_logs() {
    local service=${1:-""}
    local project_root="$(get_project_root)"
    
    cd "$project_root"
    
    if [ -z "$service" ]; then
        docker compose -f docker/compose.yaml logs -f
    else
        docker compose -f docker/compose.yaml logs -f "$service"
    fi
}

# Obtener estado de contenedores
docker_status() {
    local project_root="$(get_project_root)"
    
    cd "$project_root"
    docker compose -f docker/compose.yaml ps
}

# Limpiar sistema de Docker
docker_cleanup() {
    echo -e "${YELLOW}Limpiando Docker...${NC}"
    
    # Parar contenedores
    docker compose -f "$(get_compose_file)" down -v
    
    # Limpiar imágenes sin usar
    docker image prune -f
    
    # Limpiar volúmenes sin usar
    docker volume prune -f
    
    echo -e "${GREEN}✓${NC} Limpieza completada"
}

# Exportar funciones
export -f get_project_root
export -f check_docker
export -f get_compose_file
export -f wait_for_service
export -f docker_exec
export -f docker_logs
export -f docker_status
export -f docker_cleanup

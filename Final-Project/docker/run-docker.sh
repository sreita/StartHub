#!/bin/bash

# StartHub Docker Compose Wrapper Script
# Simplifies running docker compose from any location
# Usage: ./run-docker.sh [command]
# Example: ./run-docker.sh up -d --build

set -e

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPOSE_FILE="$SCRIPT_DIR/compose.yaml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Show banner
show_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║     StartHub Docker Compose Helper     ║"
    echo "║                                        ║"
    echo "║  Services: Frontend, Spring Auth,     ║"
    echo "║             FastAPI, MySQL, MailHog    ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Show help
show_help() {
    echo -e "${BLUE}Available commands:${NC}"
    echo ""
    echo -e "  ${GREEN}./run-docker.sh up${NC}                 - Start services in foreground"
    echo -e "  ${GREEN}./run-docker.sh up -d${NC}              - Start services in background"
    echo -e "  ${GREEN}./run-docker.sh up -d --build${NC}      - Start and rebuild images"
    echo -e "  ${GREEN}./run-docker.sh ps${NC}                 - View container status"
    echo -e "  ${GREEN}./run-docker.sh logs${NC}               - View logs in real-time"
    echo -e "  ${GREEN}./run-docker.sh logs [service]${NC}    - View logs for specific service"
    echo -e "  ${GREEN}./run-docker.sh stop${NC}               - Stop all services"
    echo -e "  ${GREEN}./run-docker.sh down${NC}               - Stop and remove containers"
    echo -e "  ${GREEN}./run-docker.sh down -v${NC}            - Stop, remove, and clean volumes"
    echo -e "  ${GREEN}./run-docker.sh build${NC}              - Rebuild images without starting"
    echo -e "  ${GREEN}./run-docker.sh build --no-cache${NC}   - Rebuild without cache"
    echo -e "  ${GREEN}./run-docker.sh restart${NC}            - Restart services"
    echo -e "  ${GREEN}./run-docker.sh exec [service] [cmd]${NC} - Execute command in container"
    echo -e "  ${GREEN}./run-docker.sh help${NC}               - Show this help"
    echo ""
    echo -e "${YELLOW}Service URLs after starting:${NC}"
    echo "  Frontend:        http://localhost:3000"
    echo "  FastAPI Docs:    http://localhost:8000/docs"
    echo "  Spring Swagger:  http://localhost:8081/swagger-ui.html"
    echo "  MailHog:         http://localhost:8025"
    echo "  MySQL:           localhost:3307 (password: startHub123)"
    echo ""
}

# Check dependencies
check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}✗ Docker is not installed${NC}"
        echo "  Download from: https://www.docker.com/products/docker-desktop"
        return 1
    fi
    echo -e "${GREEN}✓ Docker${NC}"
    
    if ! command -v docker compose &> /dev/null; then
        echo -e "${RED}✗ Docker Compose is not installed${NC}"
        echo "  Included in Docker Desktop version 1.20.0+"
        return 1
    fi
    echo -e "${GREEN}✓ Docker Compose${NC}"
    
    if ! docker ps &> /dev/null; then
        echo -e "${RED}✗ Docker daemon is not running${NC}"
        echo "  Please start Docker Desktop"
        return 1
    fi
    echo -e "${GREEN}✓ Docker daemon active${NC}"
    
    echo ""
}

# Check compose file
check_compose_file() {
    if [ ! -f "$COMPOSE_FILE" ]; then
        echo -e "${RED}✗ compose.yaml not found at $COMPOSE_FILE${NC}"
        return 1
    fi
    echo -e "${GREEN}✓ compose.yaml found${NC}"
    echo ""
}

# Show status
show_status() {
    echo -e "${BLUE}Service status:${NC}"
    docker compose -f "$COMPOSE_FILE" ps
    echo ""
}

# Main
main() {
    show_banner
    
    # If no args or help, show help
    if [ $# -eq 0 ] || [ "$1" = "help" ] || [ "$1" = "-h" ]; then
        show_help
        return 0
    fi
    
    # Check dependencies
    if ! check_dependencies; then
        echo -e "${RED}Could not verify required dependencies.${NC}"
        return 1
    fi
    
    # Check compose file
    if ! check_compose_file; then
        return 1
    fi
    
    # Process command
    COMMAND="$1"
    
    case "$COMMAND" in
        up)
            shift
            echo -e "${YELLOW}Starting services...${NC}"
            docker compose -f "$COMPOSE_FILE" up "$@"
            ;;
        down)
            shift
            echo -e "${YELLOW}Stopping services...${NC}"
            docker compose -f "$COMPOSE_FILE" down "$@"
            ;;
        stop)
            echo -e "${YELLOW}Stopping services...${NC}"
            docker compose -f "$COMPOSE_FILE" stop
            ;;
        restart)
            echo -e "${YELLOW}Restarting services...${NC}"
            docker compose -f "$COMPOSE_FILE" restart
            echo -e "${GREEN}Services restarted${NC}"
            ;;
        ps)
            show_status
            ;;
        logs)
            shift
            docker compose -f "$COMPOSE_FILE" logs -f "$@"
            ;;
        build)
            shift
            echo -e "${YELLOW}Building images...${NC}"
            docker compose -f "$COMPOSE_FILE" build "$@"
            echo -e "${GREEN}Build completed${NC}"
            ;;
        exec)
            shift
            docker compose -f "$COMPOSE_FILE" exec "$@"
            ;;
        *)
            # Pass command directly to docker compose
            docker compose -f "$COMPOSE_FILE" "$@"
            ;;
    esac
}

# Run main
main "$@"

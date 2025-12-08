#!/bin/bash

################################################################################
#                                                                              #
#  ACTUALIZAR TESTS - Reorganiza tests en carpetas                            #
#                                                                              #
################################################################################

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Reorganizando tests en carpetas...${NC}"
echo ""

# Mover tests de integración
echo "Moviendo tests de integración..."
mv -v test_all_features.sh integration/ 2>/dev/null || true
mv -v test_flow.sh integration/ 2>/dev/null || true
mv -v test_complete_system.sh integration/ 2>/dev/null || true
mv -v test_authentication.sh integration/ 2>/dev/null || true
mv -v test_startups.sh integration/ 2>/dev/null || true
mv -v test_interactions.sh integration/ 2>/dev/null || true

# Mover tests E2E
echo "Moviendo tests E2E..."
mv -v test_docker.sh e2e/ 2>/dev/null || true
mv -v test_docker_e2e.sh e2e/ 2>/dev/null || true
mv -v test_frontend.sh e2e/ 2>/dev/null || true

# Mover tests unitarios
echo "Moviendo tests unitarios..."
mv -v test_crud_complete.py unit/ 2>/dev/null || true
mv -v test_manual.py unit/ 2>/dev/null || true
mv -v test_search.py unit/ 2>/dev/null || true
mv -v test_users_startups.py unit/ 2>/dev/null || true
mv -v test_votes_comments.py unit/ 2>/dev/null || true
mv -v test_backend.sh unit/ 2>/dev/null || true

echo ""
echo -e "${GREEN}✓${NC} Tests reorganizados en carpetas"
echo ""
echo "Estructura resultante:"
echo "  integration/ - Tests de integración entre servicios"
echo "  e2e/         - Tests end-to-end y Docker"
echo "  unit/        - Tests unitarios"

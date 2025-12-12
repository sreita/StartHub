@echo off
REM StartHub Docker Compose Wrapper Script for Windows
REM Simplifica la ejecuci贸n de docker compose desde cualquier ubicaci贸n
REM Uso: run-docker.bat [comando]
REM Ejemplo: run-docker.bat up -d --build

setlocal enabledelayedexpansion

REM Obtener directorio del script
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "COMPOSE_FILE=%SCRIPT_DIR%compose.yaml"

REM Definir colores (Windows 10+ con soporte ANSI)
set "RESET=[0m"
set "RED=[0;31m"
set "GREEN=[0;32m"
set "YELLOW=[1;33m"
set "BLUE=[0;34m"

REM Función para mostrar banner
call :show_banner
exit /b 0

REM FUNCIONES
:show_banner
echo.
echo %BLUE%╔════════════════════════════════════════╗
echo %BLUE%║     StartHub Docker Compose Helper     ║
echo %BLUE%║                                        ║
echo %BLUE%║  Servicios: Frontend, Spring Auth,     ║
echo %BLUE%║             FastAPI, MySQL, MailHog    ║
echo %BLUE%╚════════════════════════════════════════╝%RESET%
echo.

if "%1"=="" goto show_help
if "%1"=="help" goto show_help
if "%1"=="-h" goto show_help

call :check_dependencies
if errorlevel 1 goto error_end

call :check_compose_file
if errorlevel 1 goto error_end

set "COMMAND=%1"

if "%COMMAND%"=="up" goto cmd_up
if "%COMMAND%"=="down" goto cmd_down
if "%COMMAND%"=="stop" goto cmd_stop
if "%COMMAND%"=="restart" goto cmd_restart
if "%COMMAND%"=="ps" goto cmd_ps
if "%COMMAND%"=="logs" goto cmd_logs
if "%COMMAND%"=="build" goto cmd_build
if "%COMMAND%"=="exec" goto cmd_exec

REM Comando no reconocido, pasar a docker compose directamente
shift
docker compose -f "%COMPOSE_FILE%" %COMMAND% %*
goto end

:cmd_up
shift
echo %YELLOW%Iniciando servicios...%RESET%
docker compose -f "%COMPOSE_FILE%" up %*
goto end

:cmd_down
shift
echo %YELLOW%Parando servicios...%RESET%
docker compose -f "%COMPOSE_FILE%" down %*
call :show_help
goto end

:cmd_stop
echo %YELLOW%Deteniendo servicios...%RESET%
docker compose -f "%COMPOSE_FILE%" stop
goto end

:cmd_restart
echo %YELLOW%Reiniciando servicios...%RESET%
docker compose -f "%COMPOSE_FILE%" restart
echo %GREEN%Servicios reiniciados%RESET%
goto end

:cmd_ps
call :show_status
goto end

:cmd_logs
shift
docker compose -f "%COMPOSE_FILE%" logs -f %*
goto end

:cmd_build
shift
echo %YELLOW%Construyendo imágenes...%RESET%
docker compose -f "%COMPOSE_FILE%" build %*
echo %GREEN%Construcción completada%RESET%
goto end

:cmd_exec
shift
docker compose -f "%COMPOSE_FILE%" exec %*
goto end

:show_help
echo %BLUE%Comandos disponibles:%RESET%
echo.
echo   %GREEN%run-docker.bat up%RESET%                 - Iniciar servicios en primer plano
echo   %GREEN%run-docker.bat up -d%RESET%              - Iniciar servicios en background
echo   %GREEN%run-docker.bat up -d --build%RESET%      - Iniciar y reconstruir imágenes
echo   %GREEN%run-docker.bat ps%RESET%                 - Ver estado de contenedores
echo   %GREEN%run-docker.bat logs%RESET%               - Ver logs en tiempo real
echo   %GREEN%run-docker.bat logs [servicio]%RESET%    - Ver logs de un servicio específico
echo   %GREEN%run-docker.bat stop%RESET%               - Parar todos los servicios
echo   %GREEN%run-docker.bat down%RESET%               - Parar y remover contenedores
echo   %GREEN%run-docker.bat down -v%RESET%            - Parar, remover y limpiar volúmenes
echo   %GREEN%run-docker.bat build%RESET%              - Reconstruir imágenes sin iniciar
echo   %GREEN%run-docker.bat build --no-cache%RESET%   - Reconstruir sin caché
echo   %GREEN%run-docker.bat restart%RESET%            - Reiniciar servicios
echo   %GREEN%run-docker.bat exec [servicio] [cmd]%RESET% - Ejecutar comando en contenedor
echo   %GREEN%run-docker.bat help%RESET%               - Mostrar esta ayuda
echo.
echo %YELLOW%URLs de servicios después de iniciar:%RESET%
echo   Frontend:        http://localhost:3000
echo   FastAPI Docs:    http://localhost:8000/docs
echo   Spring Swagger:  http://localhost:8081/swagger-ui.html
echo   MailHog:         http://localhost:8025
echo   MySQL:           localhost:3307 (password: startHub123)
echo.
goto end

:check_dependencies
echo %BLUE%Verificando dependencias...%RESET%

where docker >nul 2>nul
if errorlevel 1 (
    echo %RED%✗ Docker no está instalado%RESET%
    echo   Descarga desde: https://www.docker.com/products/docker-desktop
    exit /b 1
)
echo %GREEN%✓ Docker%RESET%

where docker-compose >nul 2>nul
if errorlevel 1 (
    where "docker compose" >nul 2>nul
    if errorlevel 1 (
        echo %RED%✗ Docker Compose no está instalado%RESET%
        echo   Incluido en Docker Desktop versión 1.20.0+
        exit /b 1
    )
)
echo %GREEN%✓ Docker Compose%RESET%

docker ps >nul 2>nul
if errorlevel 1 (
    echo %RED%✗ Docker daemon no está ejecutándose%RESET%
    echo   Por favor inicia Docker Desktop
    exit /b 1
)
echo %GREEN%✓ Docker daemon activo%RESET%
echo.
exit /b 0

:check_compose_file
if not exist "%COMPOSE_FILE%" (
    echo %RED%✗ Archivo compose.yaml no encontrado en %COMPOSE_FILE%%RESET%
    exit /b 1
)
echo %GREEN%✓ Archivo compose.yaml encontrado%RESET%
echo.
exit /b 0

:show_status
echo %BLUE%Estado de servicios:%RESET%
docker compose -f "%COMPOSE_FILE%" ps
echo.
echo %BLUE%Verificación de conectividad:%RESET%

REM Frontend
curl -s http://localhost:3000 >nul 2>nul
if %errorlevel% equ 0 (
    echo %GREEN%✓ Frontend%RESET% (http://localhost:3000)
) else (
    echo %YELLOW%⚠ Frontend%RESET% (no responde)
)

REM FastAPI
curl -s http://localhost:8000/docs >nul 2>nul
if %errorlevel% equ 0 (
    echo %GREEN%✓ FastAPI%RESET% (http://localhost:8000/docs)
) else (
    echo %YELLOW%⚠ FastAPI%RESET% (no responde)
)

REM Spring Auth
curl -s http://localhost:8081/swagger-ui.html >nul 2>nul
if %errorlevel% equ 0 (
    echo %GREEN%✓ Spring Auth%RESET% (http://localhost:8081/swagger-ui.html)
) else (
    echo %YELLOW%⚠ Spring Auth%RESET% (no responde)
)

REM MailHog
curl -s http://localhost:8025 >nul 2>nul
if %errorlevel% equ 0 (
    echo %GREEN%✓ MailHog%RESET% (http://localhost:8025)
) else (
    echo %YELLOW%⚠ MailHog%RESET% (no responde)
)
echo.
exit /b 0

:error_end
echo.
echo %RED%No se pudieron verificar las dependencias requeridas.%RESET%
exit /b 1

:end
endlocal
exit /b 0

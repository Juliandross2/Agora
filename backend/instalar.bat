@echo off
echo ========================================
echo    INSTALADOR AGORA BACKEND
echo ========================================
echo.
echo Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker no está instalado.
    echo Por favor instale Docker Desktop desde: https://docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker encontrado!
echo.
echo Iniciando servicios...
docker-compose down -v
docker-compose up -d --build

echo.
echo ========================================
echo   INSTALACION COMPLETADA
echo ========================================
echo.
echo El backend está ejecutándose en:
echo   http://localhost:8000
echo.
echo Para ver documentación API:
echo   http://localhost:8000/api/docs/swagger/
echo.
echo Para detener el servicio, ejecute: detener.bat
echo.
pause
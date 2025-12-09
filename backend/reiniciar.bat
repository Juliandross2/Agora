@echo off
echo Reiniciando servicios Agora...
docker-compose restart
echo.
echo Servicios reiniciados.
echo Backend disponible en: http://localhost:8000
pause
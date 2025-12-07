# Instrucciones de Despliegue

## Requisitos Previos
- Docker instalado
- Docker Compose instalado

## Pasos de Instalación

1. Extrae los archivos del proyecto
2. Abre una terminal en la carpeta del proyecto
3. Ejecuta:
   ```bash
   docker-compose up --build
   ```

4. En otra terminal, ejecuta migraciones (primera vez):
   ```bash
   docker-compose exec django python manage.py migrate
   ```

5. Accede a: `http://localhost:8000`

## Detener la aplicación
```bash
docker-compose down
```
# Agora
Programa para facilitar el proceso de comparar pemsa en el contexto del proceso de electivas de la facultad de electrónica de la Universidad del Cauca


## Pasos para conectar el backend

### 1. Clonar el repositorio
```bash
git clone https://github.com/Juliandross2/Agora.git
cd Agora/backend
```
### 2. Crear el entorno virtual
```bash
# Crear entorno virtual
python -m venv .venv
```
# Activar entorno virtual
```bash
# En Windows:
.venv\Scripts\Activate.bat
```
```bash
# En macOS/Linux:
source .venv/bin/activate
```
### 3. Instalar dependencias
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```
### 4. Configurar BD 
(esto aplica para motor local, si quieres hacerlo con docket adelante)

```bash
# Entrar a la consola de la BD como administrador
mysql -u root -p
```
# Crear base de datos
```sql
CREATE DATABASE agora_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'agora_user'@'localhost' IDENTIFIED BY 'agora_password';
GRANT ALL PRIVILEGES ON agora_db.* TO 'agora_user'@'localhost';
FLUSH PRIVILEGES;
```
# Crea tu .env en la raíz del backend 
(no confundir con el venv)
```env
# MySQL variables
DB_NAME=agora_db
DB_USER=<tu usuario>
DB_PASSWORD=<tu contraseña>
DB_HOST=localhost
DB_PORT=3306
```
### 5. Corre el backend y testea si funciona
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejectuar servidor
python manage.py runserver 0.0.0.0:8000
```
- Ejecuta en postman o tu herramienta de peticiones de confianza
http://localhost:8000/api/usuario/test/

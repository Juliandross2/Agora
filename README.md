# Agora
Programa para facilitar el proceso de comparar pemsa en el contexto del proceso de electivas de la facultad de electrónica de la Universidad del Cauca
## Pasos para conectar el frontend
cd "d:\Ingenieria\8vo semestre\Agora\frontend\agora_frontend"

### instalar runtime y router + vite
npm install react-dom react-router-dom

### instalar Vite (dev) y plugin react si usas Vite
npm install -D vite @vitejs/plugin-react

### instalar Tailwind y PostCSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

### instalar icon set que el layout sugiere (lucide)
npm install lucide-react


## Pasos para conectar el backend

### 1. Clonar el repositorio
(terminal)
git clone https://github.com/Juliandross2/Agora.git
cd Agora/backend

### 2. Crear el entorno virtual
(terminal)
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\Activate.bat

# En macOS/Linux:
source .venv/bin/activate

### 3. Instalar dependencias
(terminal)
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

### 4. Configurar BD 
(esto aplica para motor local, si quieres hacerlo con docket adelante)

(terminal)
# Entrar a la consola de la BD como administrador
mysql -u root -p

# Crear base de datos
CREATE DATABASE agora_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'agora_user'@'localhost' IDENTIFIED BY 'agora_password';
GRANT ALL PRIVILEGES ON agora_db.* TO 'agora_user'@'localhost';
FLUSH PRIVILEGES;

# Crea tu .env en la raíz del backend 
(no confundir con el venv)
(codigo)
# MySQL variables
DB_NAME=agora_db
DB_USER=<tu usuario>
DB_PASSWORD=<tu contraseña>
DB_HOST=localhost
DB_PORT=3306

### 5. Corre el backend y testea si funciona
(terminal)
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejectuar servidor
python manage.py runserver 0.0.0.0:8000

# Ejecuta en postman o tu herramienta de peticiones de confianza
http://localhost:8000/api/usuario/test/
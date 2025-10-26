--- MySQL script for creating the database and user for the Django application ---
DROP DATABASE IF EXISTS agora_db;
CREATE DATABASE IF NOT EXISTS agora_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agora_db;
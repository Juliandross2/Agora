-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: agora_db
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `api_electiva`
--

DROP TABLE IF EXISTS `api_electiva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_electiva` (
  `electiva_id` int NOT NULL AUTO_INCREMENT,
  `nombre_electiva` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `es_activa` tinyint(1) NOT NULL,
  `programa_id_id` int NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`electiva_id`),
  KEY `api_electiva_programa_id_id_d647afd4_fk_api_programa_programa_id` (`programa_id_id`),
  CONSTRAINT `api_electiva_programa_id_id_d647afd4_fk_api_programa_programa_id` FOREIGN KEY (`programa_id_id`) REFERENCES `api_programa` (`programa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_electiva`
--

LOCK TABLES `api_electiva` WRITE;
/*!40000 ALTER TABLE `api_electiva` DISABLE KEYS */;
INSERT INTO `api_electiva` VALUES (1,'Machine Learning y Deep Learning',0,1,NULL);
/*!40000 ALTER TABLE `api_electiva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_materia`
--

DROP TABLE IF EXISTS `api_materia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_materia` (
  `materia_id` int NOT NULL AUTO_INCREMENT,
  `nombre_materia` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `creditos` int NOT NULL,
  `es_obligatoria` tinyint(1) NOT NULL,
  `es_activa` tinyint(1) NOT NULL,
  `pensum_id_id` int NOT NULL,
  `semestre` int NOT NULL,
  PRIMARY KEY (`materia_id`),
  KEY `api_materia_pensum_id_id_4ea0836c_fk_api_pensum_pensum_id` (`pensum_id_id`),
  CONSTRAINT `api_materia_pensum_id_id_4ea0836c_fk_api_pensum_pensum_id` FOREIGN KEY (`pensum_id_id`) REFERENCES `api_pensum` (`pensum_id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_materia`
--

LOCK TABLES `api_materia` WRITE;
/*!40000 ALTER TABLE `api_materia` DISABLE KEYS */;
INSERT INTO `api_materia` VALUES (2,'Cálculo I',4,1,1,1,1),(3,'Introducción a la Informática',3,1,1,1,1),(4,'Introducción a la Ingeniería de Sistemas',1,1,1,1,1),(5,'Laboratorio de Introducción a la Informática',1,1,1,1,1),(6,'Lectura y Escritura',2,1,1,1,1),(7,'FISH 1',2,1,1,1,1),(8,'Álgebra Lineal',4,1,1,1,2),(9,'Cálculo II',4,1,1,1,2),(10,'Laboratorio de Mecánica',1,1,1,1,2),(11,'Laboratorio de Programación Orientada a Objetos',1,1,1,1,2),(12,'Mecánica',3,1,1,1,2),(13,'Programación Orientada a Objetos',3,1,1,1,2),(14,'FISH 2',2,1,1,1,2),(15,'Cálculo III',4,1,1,1,3),(16,'Electromagnetismo',3,1,1,1,3),(17,'Estructuras de Datos I',3,1,1,1,3),(18,'Laboratorio de Electromagnetismo',1,1,1,1,3),(19,'Laboratorio de Estructuras de Datos I',1,1,1,1,3),(20,'FISH 3',2,1,1,1,3),(21,'Bases de Datos I',3,1,1,1,4),(22,'Ecuaciones Diferenciales Ordinarias',4,1,1,1,4),(23,'Estructura de Datos II',3,1,1,1,4),(24,'Laboratorio de Bases de Datos I',1,1,1,1,4),(25,'Laboratorio de Estructuras de Datos II',1,1,1,1,4),(26,'Vibraciones y Ondas',3,1,1,1,4),(27,'Análisis Numérico',4,1,1,1,5),(28,'Arquitectura Computacional',4,1,1,1,5),(29,'Bases de Datos II',3,1,1,1,5),(30,'Ingeniería de Software I',3,1,1,1,5),(31,'Laboratorio de Bases de Datos II',1,1,1,1,5),(32,'Laboratorio de Ingeniería de Software I',1,1,1,1,5),(33,'Teoría de la Computación',3,1,1,1,5),(34,'Estadística y Probabilidad',4,1,1,1,6),(35,'Estructura de Lenguajes',3,1,1,1,6),(36,'Ingeniería de Software II',3,1,1,1,6),(37,'Laboratorio de Estructura de Lenguajes',1,1,1,1,6),(38,'Laboratorio de Ingeniería de Software II',1,1,1,1,6),(39,'Sistemas Operativos',3,1,1,1,6),(40,'Laboratorio de Sistemas Operativos',1,1,1,1,6),(41,'Ingeniería de Software III',3,1,1,1,7),(42,'Inteligencia Artificial',3,1,1,1,7),(43,'Laboratorio de Ingeniería de Software III',1,1,1,1,7),(44,'Laboratorio de Sistemas Distribuidos',1,1,1,1,7),(45,'Metodología de la Investigación',3,1,1,1,7),(46,'Sistemas Distribuidos',3,1,1,1,7),(47,'Teoría y Dinámica de Sistemas',3,1,1,1,7),(48,'Calidad de Software',3,1,1,1,8),(49,'Electiva I',3,0,1,1,8),(50,'Electiva II',3,0,1,1,8),(51,'Investigación de Operaciones',4,1,1,1,8),(52,'Proyecto I',3,1,1,1,8),(53,'Redes',3,1,1,1,8),(54,'Electiva III',3,0,1,1,9),(55,'Electiva IV',3,0,1,1,9),(56,'Fundamentos de Economía',3,1,1,1,9),(57,'Gestión de Proyectos Informáticos',3,1,1,1,9),(58,'Gestión Empresarial',3,1,1,1,9),(59,'Legislación Laboral',1,1,1,1,9),(60,'Proyecto II',3,1,1,1,9),(61,'Electiva V',3,0,1,1,10),(62,'Ética',2,1,1,1,10),(63,'Trabajo de Grado',14,1,1,1,10);
/*!40000 ALTER TABLE `api_materia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_ofertaelectiva`
--

DROP TABLE IF EXISTS `api_ofertaelectiva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_ofertaelectiva` (
  `oferta_electiva_id` int NOT NULL AUTO_INCREMENT,
  `periodo` int NOT NULL,
  `es_activa` tinyint(1) NOT NULL,
  `electiva_id_id` int NOT NULL,
  `materia_id_id` int NOT NULL,
  PRIMARY KEY (`oferta_electiva_id`),
  KEY `api_ofertaelectiva_electiva_id_id_a497a99d_fk_api_elect` (`electiva_id_id`),
  KEY `api_ofertaelectiva_materia_id_id_74d920df_fk_api_mater` (`materia_id_id`),
  CONSTRAINT `api_ofertaelectiva_electiva_id_id_a497a99d_fk_api_elect` FOREIGN KEY (`electiva_id_id`) REFERENCES `api_electiva` (`electiva_id`),
  CONSTRAINT `api_ofertaelectiva_materia_id_id_74d920df_fk_api_mater` FOREIGN KEY (`materia_id_id`) REFERENCES `api_materia` (`materia_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_ofertaelectiva`
--

LOCK TABLES `api_ofertaelectiva` WRITE;
/*!40000 ALTER TABLE `api_ofertaelectiva` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_ofertaelectiva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_pensum`
--

DROP TABLE IF EXISTS `api_pensum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_pensum` (
  `pensum_id` int NOT NULL AUTO_INCREMENT,
  `anio_creacion` int DEFAULT NULL,
  `es_activo` tinyint(1) NOT NULL,
  `programa_id_id` int NOT NULL,
  PRIMARY KEY (`pensum_id`),
  KEY `api_pensum_programa_id_id_4e5335ff_fk_api_programa_programa_id` (`programa_id_id`),
  CONSTRAINT `api_pensum_programa_id_id_4e5335ff_fk_api_programa_programa_id` FOREIGN KEY (`programa_id_id`) REFERENCES `api_programa` (`programa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_pensum`
--

LOCK TABLES `api_pensum` WRITE;
/*!40000 ALTER TABLE `api_pensum` DISABLE KEYS */;
INSERT INTO `api_pensum` VALUES (1,2024,1,1),(2,2025,1,2);
/*!40000 ALTER TABLE `api_pensum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_programa`
--

DROP TABLE IF EXISTS `api_programa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_programa` (
  `programa_id` int NOT NULL AUTO_INCREMENT,
  `nombre_programa` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `es_activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`programa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_programa`
--

LOCK TABLES `api_programa` WRITE;
/*!40000 ALTER TABLE `api_programa` DISABLE KEYS */;
INSERT INTO `api_programa` VALUES (1,'Ingeniería Sistemas',1),(2,'Ingeniería Electronica',1);
/*!40000 ALTER TABLE `api_programa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_usuario`
--

DROP TABLE IF EXISTS `api_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_usuario` (
  `usuario_id` int NOT NULL AUTO_INCREMENT,
  `contrasenia` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_usuario` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_usuario` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `es_activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`usuario_id`),
  UNIQUE KEY `email_usuario` (`email_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_usuario`
--

LOCK TABLES `api_usuario` WRITE;
/*!40000 ALTER TABLE `api_usuario` DISABLE KEYS */;
INSERT INTO `api_usuario` VALUES (1,'pbkdf2_sha256$1000000$rBCLa0IKrJAPATN4MVXSIB$VN3CZs8KurxFNE0vRRBrG3h1pRtk85ijVB4WiYEq7i4=','Test User','test@ejemplo.com',1),(2,'pbkdf2_sha256$1000000$kAMUv8MefAwVIyMxrlrQY6$aWxxmiuPXF0GOhyKs8njhaEuJ3Qd9F7ghIwPzgmyyME=','john_doe','john.doe@example.com',1),(3,'pbkdf2_sha256$1000000$Vljr51DPvzhwgG0y911mVu$AKhGC7PYkRP3O+y7KC+QIlfdqvWTbUD71/LoPE8CYX0=','Carlos Ardila','cardila@unicauca.edu.co',1),(4,'pbkdf2_sha256$1000000$vBQGDCWPhkHoaRoHODa6yt$81neIs9ihGvo5dZbxduWRca0Rq3JsGVIaK/uR4iBbTA=','Carlos Ardila2','cardila2@unicauca.edu.co',1);
/*!40000 ALTER TABLE `api_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add electiva',7,'add_electiva'),(26,'Can change electiva',7,'change_electiva'),(27,'Can delete electiva',7,'delete_electiva'),(28,'Can view electiva',7,'view_electiva'),(29,'Can add materia',8,'add_materia'),(30,'Can change materia',8,'change_materia'),(31,'Can delete materia',8,'delete_materia'),(32,'Can view materia',8,'view_materia'),(33,'Can add pensum',9,'add_pensum'),(34,'Can change pensum',9,'change_pensum'),(35,'Can delete pensum',9,'delete_pensum'),(36,'Can view pensum',9,'view_pensum'),(37,'Can add programa',10,'add_programa'),(38,'Can change programa',10,'change_programa'),(39,'Can delete programa',10,'delete_programa'),(40,'Can view programa',10,'view_programa'),(41,'Can add usuario',11,'add_usuario'),(42,'Can change usuario',11,'change_usuario'),(43,'Can delete usuario',11,'delete_usuario'),(44,'Can view usuario',11,'view_usuario'),(45,'Can add oferta electiva',12,'add_ofertaelectiva'),(46,'Can change oferta electiva',12,'change_ofertaelectiva'),(47,'Can delete oferta electiva',12,'delete_ofertaelectiva'),(48,'Can view oferta electiva',12,'view_ofertaelectiva'),(49,'Can add Configuración de Elegibilidad',13,'add_configuracionelegibilidad'),(50,'Can change Configuración de Elegibilidad',13,'change_configuracionelegibilidad'),(51,'Can delete Configuración de Elegibilidad',13,'delete_configuracionelegibilidad'),(52,'Can view Configuración de Elegibilidad',13,'view_configuracionelegibilidad');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `configuracion_elegibilidad`
--

DROP TABLE IF EXISTS `configuracion_elegibilidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuracion_elegibilidad` (
  `configuracion_id` int NOT NULL AUTO_INCREMENT,
  `porcentaje_avance_minimo` decimal(5,4) NOT NULL,
  `nota_aprobatoria` decimal(3,1) NOT NULL,
  `semestre_limite_electivas` int NOT NULL,
  `niveles_creditos_periodos` json NOT NULL,
  `es_activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_actualizacion` datetime(6) NOT NULL,
  `programa_id` int NOT NULL,
  PRIMARY KEY (`configuracion_id`),
  KEY `configuraci_program_c19b4f_idx` (`programa_id`,`es_activo`),
  KEY `configuraci_es_acti_ac8123_idx` (`es_activo`),
  CONSTRAINT `configuracion_elegib_programa_id_8fed189c_fk_api_progr` FOREIGN KEY (`programa_id`) REFERENCES `api_programa` (`programa_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `configuracion_elegibilidad`
--

LOCK TABLES `configuracion_elegibilidad` WRITE;
/*!40000 ALTER TABLE `configuracion_elegibilidad` DISABLE KEYS */;
INSERT INTO `configuracion_elegibilidad` VALUES (2,0.6000,3.2,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-25 01:01:17.978450','2025-11-25 01:01:17.978477',1),(3,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-25 01:01:39.505886','2025-11-25 01:01:39.505922',1),(4,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-25 01:01:46.531281','2025-11-25 01:01:46.531304',1),(5,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-25 01:03:01.292618','2025-11-25 01:03:01.292896',1),(6,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-25 01:03:16.037919','2025-11-25 01:03:16.037951',1),(7,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:22:29.233213','2025-11-27 19:22:29.233285',1),(8,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:26:02.241730','2025-11-27 19:26:02.241979',1),(9,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:27:55.803859','2025-11-27 19:27:55.803936',1),(10,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:34:32.485923','2025-11-27 19:34:32.485993',1),(11,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:37:16.332242','2025-11-27 19:37:16.332308',1),(12,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:37:29.005731','2025-11-27 19:37:29.005766',1),(13,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:38:46.171909','2025-11-27 19:38:46.171971',1),(14,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:40:00.222317','2025-11-27 19:40:00.222390',1),(15,0.7000,3.3,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:40:22.938561','2025-11-27 19:40:22.938610',1),(16,0.7000,3.0,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:41:47.046052','2025-11-27 19:41:47.046136',1),(17,0.7000,3.0,5,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:43:13.076985','2025-11-27 19:43:13.077125',1),(18,0.7000,3.0,7,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:43:44.586986','2025-11-27 19:43:44.587104',1),(19,0.7000,3.0,7,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',0,'2025-11-27 19:55:07.333325','2025-11-27 19:55:07.333385',1),(20,0.7000,3.0,8,'{\"8\": {\"max_periodos\": 7, \"min_creditos\": 112}, \"9\": {\"max_periodos\": 8, \"min_creditos\": 132}, \"10\": {\"max_periodos\": 9, \"min_creditos\": 151}}',1,'2025-11-27 19:56:24.796694','2025-11-27 19:56:24.796763',1);
/*!40000 ALTER TABLE `configuracion_elegibilidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(13,'api','configuracionelegibilidad'),(7,'api','electiva'),(8,'api','materia'),(12,'api','ofertaelectiva'),(9,'api','pensum'),(10,'api','programa'),(11,'api','usuario'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-22 20:26:48.235523'),(2,'auth','0001_initial','2025-10-22 20:26:49.301074'),(3,'admin','0001_initial','2025-10-22 20:26:49.534294'),(4,'admin','0002_logentry_remove_auto_add','2025-10-22 20:26:49.544356'),(5,'admin','0003_logentry_add_action_flag_choices','2025-10-22 20:26:49.553084'),(6,'api','0001_initial','2025-10-22 20:26:50.200467'),(7,'contenttypes','0002_remove_content_type_name','2025-10-22 20:26:50.353517'),(8,'auth','0002_alter_permission_name_max_length','2025-10-22 20:26:50.447479'),(9,'auth','0003_alter_user_email_max_length','2025-10-22 20:26:50.473708'),(10,'auth','0004_alter_user_username_opts','2025-10-22 20:26:50.483040'),(11,'auth','0005_alter_user_last_login_null','2025-10-22 20:26:50.562592'),(12,'auth','0006_require_contenttypes_0002','2025-10-22 20:26:50.567976'),(13,'auth','0007_alter_validators_add_error_messages','2025-10-22 20:26:50.576612'),(14,'auth','0008_alter_user_username_max_length','2025-10-22 20:26:50.672737'),(15,'auth','0009_alter_user_last_name_max_length','2025-10-22 20:26:50.775964'),(16,'auth','0010_alter_group_name_max_length','2025-10-22 20:26:50.799887'),(17,'auth','0011_update_proxy_permissions','2025-10-22 20:26:50.814586'),(18,'auth','0012_alter_user_first_name_max_length','2025-10-22 20:26:50.918519'),(19,'sessions','0001_initial','2025-10-22 20:26:50.976388'),(20,'api','0002_electiva_descripcion','2025-11-17 19:35:24.585043'),(21,'api','0003_configuracionelegibilidad','2025-11-17 19:35:24.705757'),(22,'api','0004_remove_total_creditos_obligatorios','2025-11-27 19:53:25.001696'),(23,'api','0005_programa_id_required','2025-11-27 20:38:37.603607'),(24,'api','0006_fix_programa_id_column_name','2025-11-27 20:41:07.353952');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-07 13:02:08

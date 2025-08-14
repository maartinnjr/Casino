-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: shinkansen.proxy.rlwy.net    Database: railway
-- ------------------------------------------------------
-- Server version	9.4.0

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
-- Table structure for table `administradores`
--

DROP TABLE IF EXISTS `administradores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administradores` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `contrasena` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_admin`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administradores`
--

LOCK TABLES `administradores` WRITE;
/*!40000 ALTER TABLE `administradores` DISABLE KEYS */;
INSERT INTO `administradores` VALUES (1,'admincasino','adminpalacio');
/*!40000 ALTER TABLE `administradores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bancos`
--

DROP TABLE IF EXISTS `bancos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bancos` (
  `id_banco` int NOT NULL AUTO_INCREMENT,
  `nombre_banco` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_banco`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bancos`
--

LOCK TABLES `bancos` WRITE;
/*!40000 ALTER TABLE `bancos` DISABLE KEYS */;
INSERT INTO `bancos` VALUES (1,'Banco de Chile'),(2,'Banco Santander'),(3,'BancoEstado'),(4,'Scotiabank'),(5,'Banco de Crédito e Inversiones (BCI)');
/*!40000 ALTER TABLE `bancos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `canjes_dulces`
--

DROP TABLE IF EXISTS `canjes_dulces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `canjes_dulces` (
  `id_canje` int NOT NULL AUTO_INCREMENT,
  `id_admin` int NOT NULL,
  `id_usuario` int NOT NULL,
  `dulces_canjeados` int NOT NULL,
  `costo_saldo` int NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_canje`),
  KEY `id_admin` (`id_admin`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `canjes_dulces_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `administradores` (`id_admin`),
  CONSTRAINT `canjes_dulces_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canjes_dulces`
--

LOCK TABLES `canjes_dulces` WRITE;
/*!40000 ALTER TABLE `canjes_dulces` DISABLE KEYS */;
INSERT INTO `canjes_dulces` VALUES (1,1,3,6,30000,'2025-08-11 01:28:23');
/*!40000 ALTER TABLE `canjes_dulces` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comunas`
--

DROP TABLE IF EXISTS `comunas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comunas` (
  `id_comuna` int NOT NULL AUTO_INCREMENT,
  `nombre_comuna` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_comuna`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comunas`
--

LOCK TABLES `comunas` WRITE;
/*!40000 ALTER TABLE `comunas` DISABLE KEYS */;
INSERT INTO `comunas` VALUES (1,'Cerrillos'),(2,'Cerro Navia'),(3,'Conchalí'),(4,'El Bosque'),(5,'Estación Central'),(6,'Huechuraba'),(7,'Independencia'),(8,'La Cisterna'),(9,'La Florida'),(10,'La Granja'),(11,'La Pintana'),(12,'La Reina'),(13,'Las Condes'),(14,'Lo Barnechea'),(15,'Lo Espejo'),(16,'Lo Prado'),(17,'Macul'),(18,'Maipú'),(19,'Ñuñoa'),(20,'Pedro Aguirre Cerda'),(21,'Peñalolén'),(22,'Providencia'),(23,'Pudahuel'),(24,'Quilicura'),(25,'Quinta Normal'),(26,'Recoleta'),(27,'Renca'),(28,'San Joaquín'),(29,'San Miguel'),(30,'San Ramón'),(31,'Santiago'),(32,'Vitacura'),(33,'Puente Alto'),(34,'Pirque'),(35,'San José de Maipo'),(36,'Colina'),(37,'Lampa'),(38,'Tiltil'),(39,'San Bernardo'),(40,'Buin'),(41,'Calera de Tango'),(42,'Paine'),(43,'Melipilla'),(44,'Alhué'),(45,'Curacaví'),(46,'María Pinto'),(47,'San Pedro'),(48,'Talagante'),(49,'El Monte'),(50,'Isla de Maipo'),(51,'Padre Hurtado'),(52,'Peñaflor');
/*!40000 ALTER TABLE `comunas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_partidas`
--

DROP TABLE IF EXISTS `historial_partidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_partidas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_juego` int NOT NULL,
  `apuesta` int NOT NULL,
  `resultado` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_juego` (`id_juego`),
  CONSTRAINT `historial_partidas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `historial_partidas_ibfk_2` FOREIGN KEY (`id_juego`) REFERENCES `juegos` (`id_juego`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_partidas`
--

LOCK TABLES `historial_partidas` WRITE;
/*!40000 ALTER TABLE `historial_partidas` DISABLE KEYS */;
INSERT INTO `historial_partidas` VALUES (1,1,1,1000,'empate','2025-08-08 10:05:36'),(2,1,1,1000,'empate','2025-08-08 10:10:38'),(3,1,1,1000,'empate','2025-08-08 10:39:47'),(4,1,1,1000,'empate','2025-08-08 10:43:29'),(5,1,1,1000,'ganaste','2025-08-08 10:46:16'),(6,1,1,1000,'empate','2025-08-08 10:49:22'),(7,4,2,500,'ganaste','2025-08-08 10:54:40'),(8,4,3,500,'perdiste','2025-08-08 10:55:13'),(9,4,2,1000,'ganaste','2025-08-08 10:55:42'),(10,4,1,500,'perdiste','2025-08-08 10:58:00'),(11,4,3,1000,'perdiste','2025-08-08 11:00:43'),(12,4,3,1000,'perdiste','2025-08-08 11:01:04'),(13,4,2,1000,'perdiste','2025-08-08 11:01:22'),(14,4,2,1000,'perdiste','2025-08-08 11:01:38'),(15,5,1,1000,'ganaste','2025-08-08 11:09:50'),(16,5,2,100000,'perdiste','2025-08-08 11:11:10'),(17,1,1,1000,'perdiste','2025-08-08 11:14:19'),(18,1,1,1000,'ganaste','2025-08-10 23:15:40'),(19,1,1,1000,'empate','2025-08-10 23:16:37'),(20,1,2,1000,'perdiste','2025-08-10 23:22:27'),(21,1,2,1000,'perdiste','2025-08-10 23:24:52'),(22,1,2,200,'ganaste','2025-08-10 23:28:53'),(23,1,2,500,'perdiste','2025-08-10 23:29:19'),(24,1,2,500,'perdiste','2025-08-10 23:29:50'),(25,1,2,100,'ganaste','2025-08-10 23:30:05'),(26,1,1,200,'empate','2025-08-10 23:35:08'),(27,1,1,200,'empate','2025-08-10 23:35:18'),(28,1,1,100,'ganaste','2025-08-10 23:36:05'),(29,1,1,200,'ganaste','2025-08-10 23:37:24'),(30,1,1,500,'perdiste','2025-08-10 23:37:52'),(31,1,1,10,'ganaste','2025-08-10 23:38:58'),(32,1,3,10,'empate','2025-08-10 23:39:54'),(33,1,1,10,'ganaste','2025-08-10 23:41:19'),(34,1,1,100,'ganaste','2025-08-10 23:44:01'),(35,1,3,100,'empate','2025-08-10 23:48:57'),(36,1,2,1000,'ganaste','2025-08-10 23:52:06'),(37,1,3,200,'perdiste','2025-08-10 23:53:10'),(38,1,2,1000,'ganaste','2025-08-11 00:01:12'),(39,1,3,1000,'perdiste','2025-08-11 00:01:35'),(40,1,3,1000,'perdiste','2025-08-11 00:08:59'),(41,1,3,1000,'ganaste','2025-08-11 00:18:02'),(42,1,3,1000,'empate','2025-08-11 00:21:31'),(43,1,3,200,'perdiste','2025-08-11 00:24:45'),(44,1,3,1000,'perdiste','2025-08-11 00:29:15'),(46,1,4,1000,'ganaste','2025-08-11 01:03:02'),(47,1,4,1000,'ganaste','2025-08-11 01:08:46'),(48,1,1,1000,'perdiste','2025-08-11 01:28:41'),(49,1,2,1000,'ganaste','2025-08-11 01:28:57'),(50,1,3,1000,'perdiste','2025-08-11 01:29:17'),(51,1,4,1000,'perdiste','2025-08-11 01:29:32'),(52,1,1,1000,'perdiste','2025-08-11 01:31:13'),(53,1,1,1000,'empate','2025-08-11 01:31:41'),(54,1,1,1000,'ganaste','2025-08-11 01:32:39'),(55,1,2,1000,'ganaste','2025-08-11 01:33:03'),(56,1,3,1000,'ganaste','2025-08-11 01:33:29'),(57,1,4,1000,'ganaste','2025-08-11 01:33:51'),(58,6,1,1000,'ganaste','2025-08-11 12:20:28'),(59,6,2,1000,'perdiste','2025-08-11 12:20:52'),(60,6,3,1000,'empate','2025-08-11 12:21:15'),(61,6,4,1000,'ganaste','2025-08-11 12:21:32'),(62,7,1,200,'ganaste','2025-08-11 12:25:23'),(63,7,2,500,'perdiste','2025-08-11 12:26:12'),(64,7,3,500,'perdiste','2025-08-11 12:26:53'),(65,7,4,1000,'ganaste','2025-08-11 12:27:25'),(66,1,4,1000,'ganaste','2025-08-11 15:01:52'),(67,1,4,1000,'ganaste','2025-08-11 15:02:28'),(68,1,4,1000,'perdiste','2025-08-11 15:08:16'),(69,1,4,1000,'ganaste','2025-08-13 09:01:33'),(70,1,4,1000,'ganaste','2025-08-13 09:01:49'),(71,1,4,1000,'perdiste','2025-08-13 09:02:12'),(72,1,4,1000,'ganaste','2025-08-13 09:04:49'),(73,1,4,1000,'ganaste','2025-08-13 09:05:03'),(74,1,4,1000,'ganaste','2025-08-13 09:05:19'),(75,1,4,1000,'ganaste','2025-08-13 09:08:27'),(76,1,3,1000,'perdiste','2025-08-13 09:08:49'),(77,1,4,1000,'ganaste','2025-08-13 09:09:25'),(78,1,4,1000,'perdiste','2025-08-13 09:09:54'),(79,1,2,1000,'perdiste','2025-08-13 09:11:08'),(80,1,4,1000,'ganaste','2025-08-13 09:11:35'),(81,1,4,1000,'perdiste','2025-08-13 09:21:47'),(82,1,4,1000,'ganaste','2025-08-14 10:17:20');
/*!40000 ALTER TABLE `historial_partidas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `juegos`
--

DROP TABLE IF EXISTS `juegos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `juegos` (
  `id_juego` int NOT NULL AUTO_INCREMENT,
  `nombre_juego` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci,
  `apuesta_minima` int DEFAULT '100',
  PRIMARY KEY (`id_juego`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `juegos`
--

LOCK TABLES `juegos` WRITE;
/*!40000 ALTER TABLE `juegos` DISABLE KEYS */;
INSERT INTO `juegos` VALUES (1,'Blackjack','El objetivo es sumar 21 puntos o acercarse lo más posible sin pasarse.',100),(2,'Ruleta','Apuesta a un color (rojo/negro) y gana si la bola cae en tu elección.',100),(3,'Tragamonedas','Elige tu fruta de la suerte y gira los rodillos para ganar.',100),(4,'Coinflip','Apuesta a cara o sello y duplica tu monto.',100);
/*!40000 ALTER TABLE `juegos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transacciones`
--

DROP TABLE IF EXISTS `transacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transacciones` (
  `id_transaccion` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `tipo_transaccion` enum('deposito','retiro','abono') COLLATE utf8mb4_general_ci DEFAULT NULL,
  `monto` int NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_banco` int DEFAULT NULL,
  `id_canje` int DEFAULT NULL,
  PRIMARY KEY (`id_transaccion`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_banco` (`id_banco`),
  KEY `fk_transaccion_canje` (`id_canje`),
  CONSTRAINT `fk_transaccion_canje` FOREIGN KEY (`id_canje`) REFERENCES `canjes_dulces` (`id_canje`),
  CONSTRAINT `transacciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `transacciones_ibfk_2` FOREIGN KEY (`id_banco`) REFERENCES `bancos` (`id_banco`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transacciones`
--

LOCK TABLES `transacciones` WRITE;
/*!40000 ALTER TABLE `transacciones` DISABLE KEYS */;
INSERT INTO `transacciones` VALUES (1,1,'abono',12,'2025-08-10 23:14:52',NULL,NULL),(2,3,'deposito',12,'2025-08-10 23:14:52',NULL,NULL),(3,1,'abono',600,'2025-08-11 01:27:42',NULL,NULL),(4,3,'deposito',600,'2025-08-11 01:27:42',NULL,NULL),(5,3,'retiro',30000,'2025-08-11 01:28:23',NULL,1),(6,6,'abono',1000,'2025-08-11 12:19:55',NULL,NULL),(7,1,'deposito',1000,'2025-08-11 12:19:55',NULL,NULL),(8,7,'abono',100,'2025-08-11 12:24:30',NULL,NULL),(9,1,'deposito',100,'2025-08-11 12:24:30',NULL,NULL),(10,1,'abono',9000,'2025-08-11 22:10:11',NULL,NULL),(11,6,'deposito',9000,'2025-08-11 22:10:11',NULL,NULL);
/*!40000 ALTER TABLE `transacciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `contrasena` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `saldo` int NOT NULL,
  `dulces` int NOT NULL DEFAULT '0',
  `rut` varchar(12) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipo_moneda` enum('CLP','USD','EUR') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'CLP',
  `id_comuna` int DEFAULT NULL,
  `id_banco` int DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `rut` (`rut`),
  KEY `id_comuna` (`id_comuna`),
  KEY `id_banco` (`id_banco`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_comuna`) REFERENCES `comunas` (`id_comuna`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`id_banco`) REFERENCES `bancos` (`id_banco`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Martin','martinys1',95000,0,'22446506-8','Scottie Scott 589','CLP',48,3),(2,'vicente','sayko.exe',2000,0,'224307322','alejandro soto 025','CLP',48,3),(3,'sebita','seba200710',50612,6,'22576640-1','calle nueva431','CLP',52,3),(4,'tadeo','123456789',4500,0,'225710813','av pixulong 235','CLP',48,1),(5,'Renato','renato8sigma',0,0,'225199418','pedro correa ','CLP',52,1),(6,'Amy','martinteamo',30000,0,'22743879-8','Villa el alba Los Cerezos','CLP',49,3),(7,'Kenner','sofiateamo',2100,0,'28565896-9','Villa Cariño','CLP',48,3);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-14 10:20:06

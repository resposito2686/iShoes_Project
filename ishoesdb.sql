-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: ishoesdb
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `orderID` int unsigned NOT NULL AUTO_INCREMENT,
  `userID` int unsigned NOT NULL,
  `orderItems` varchar(255) NOT NULL,
  `creditCardNum` varchar(16) NOT NULL,
  `creditCardExp` varchar(5) NOT NULL,
  `creditCardSec` varchar(3) NOT NULL,
  `orderDate` date NOT NULL,
  `total` decimal(7,2) NOT NULL,
  PRIMARY KEY (`orderID`),
  KEY `userID_idx` (`userID`),
  CONSTRAINT `userID` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,2,'11 30','7676555444532231','05/25','198','2021-04-07',300.00),(2,2,'13 25','7676555444532231','05/25','198','2021-09-21',300.00),(3,2,'5 22 27','7676555444532231','05/25','198','2021-12-08',450.00);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shoes`
--

DROP TABLE IF EXISTS `shoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shoes` (
  `shoeID` int unsigned NOT NULL AUTO_INCREMENT,
  `shoeBrand` varchar(45) DEFAULT NULL,
  `shoeModel` varchar(50) DEFAULT NULL,
  `shoeColor` varchar(45) DEFAULT NULL,
  `shoeSize` int DEFAULT NULL,
  `shoePrice` decimal(6,2) DEFAULT NULL,
  `stock` int NOT NULL,
  `modelID` int unsigned NOT NULL,
  PRIMARY KEY (`shoeID`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shoes`
--

LOCK TABLES `shoes` WRITE;
/*!40000 ALTER TABLE `shoes` DISABLE KEYS */;
INSERT INTO `shoes` VALUES (1,'Nike Sneakers','Custom Air Force 1','red',5,150.00,3,0),(2,'Nike Sneakers','Custom Air Force 1','red',6,150.00,3,0),(3,'Nike Sneakers','Custom Air Force 1','red',7,150.00,3,0),(4,'Nike Sneakers','Custom Air Force 1','red',8,150.00,3,0),(5,'Nike Sneakers','Custom Air Force 1','red',9,150.00,3,0),(6,'Nike Sneakers','Custom Air Force 1','red',10,150.00,3,0),(7,'Nike Sneakers','Custom Air Force 1','red',11,150.00,3,0),(8,'Nike Sneakers','Custom Air Force 1','red',12,150.00,3,0),(9,'Nike Sneakers','Custom Air Force 1','blue',5,150.00,3,0),(10,'Nike Sneakers','Custom Air Force 1','blue',6,150.00,3,0),(11,'Nike Sneakers','Custom Air Force 1','blue',7,150.00,3,0),(12,'Nike Sneakers','Custom Air Force 1','blue',8,150.00,3,0),(13,'Nike Sneakers','Custom Air Force 1','blue',9,150.00,3,0),(14,'Nike Sneakers','Custom Air Force 1','blue',10,150.00,3,0),(15,'Nike Sneakers','Custom Air Force 1','blue',11,150.00,3,0),(16,'Nike Sneakers','Custom Air Force 1','blue',12,150.00,3,0),(17,'Nike Sneakers','Custom Air Force 1','black',5,150.00,3,0),(18,'Nike Sneakers','Custom Air Force 1','black',6,150.00,3,0),(19,'Nike Sneakers','Custom Air Force 1','black',7,150.00,3,0),(20,'Nike Sneakers','Custom Air Force 1','black',8,150.00,3,0),(21,'Nike Sneakers','Custom Air Force 1','black',9,150.00,3,0),(22,'Nike Sneakers','Custom Air Force 1','black',10,150.00,3,0),(23,'Nike Sneakers','Custom Air Force 1','black',11,150.00,3,0),(24,'Nike Sneakers','Custom Air Force 1','black',12,150.00,3,0),(25,'Nike Sneakers','Custom Air Force 1','orange',5,150.00,3,0),(26,'Nike Sneakers','Custom Air Force 1','orange',6,150.00,3,0),(27,'Nike Sneakers','Custom Air Force 1','orange',7,150.00,3,0),(28,'Nike Sneakers','Custom Air Force 1','orange',8,150.00,3,0),(29,'Nike Sneakers','Custom Air Force 1','orange',9,150.00,3,0),(30,'Nike Sneakers','Custom Air Force 1','orange',10,150.00,3,0),(31,'Nike Sneakers','Custom Air Force 1','orange',11,150.00,3,0),(32,'Nike Sneakers','Custom Air Force 1','orange',12,150.00,3,0),(33,'Nike Sneakers','Custom Air Force 1','white',5,150.00,3,0),(34,'Nike Sneakers','Custom Air Force 1','white',6,150.00,3,0),(35,'Nike Sneakers','Custom Air Force 1','white',7,150.00,3,0),(36,'Nike Sneakers','Custom Air Force 1','white',8,150.00,3,0),(37,'Nike Sneakers','Custom Air Force 1','white',9,150.00,3,0),(38,'Nike Sneakers','Custom Air Force 1','white',10,150.00,3,0),(39,'Nike Sneakers','Custom Air Force 1','white',11,150.00,3,0),(40,'Nike Sneakers','Custom Air Force 1','white',12,150.00,3,0),(41,'Converse','Chuck Taylor Allstars','black',5,90.00,2,1),(42,'Converse','Chuck Taylor Allstars','black',6,90.00,2,1),(43,'Converse','Chuck Taylor Allstars','black',7,90.00,2,1),(44,'Converse','Chuck Taylor Allstars','black',8,90.00,2,1),(45,'Converse','Chuck Taylor Allstars','black',9,90.00,2,1),(46,'Converse','Chuck Taylor Allstars','black',10,90.00,2,1),(47,'Converse','Chuck Taylor Allstars','black',11,90.00,2,1),(48,'Converse','Chuck Taylor Allstars','black',12,90.00,2,1),(49,'Converse','Chuck Taylor Allstars','blue',5,90.00,2,1),(50,'Converse','Chuck Taylor Allstars','blue',6,90.00,2,1),(51,'Converse','Chuck Taylor Allstars','blue',7,90.00,2,1),(52,'Converse','Chuck Taylor Allstars','blue',8,90.00,2,1),(53,'Converse','Chuck Taylor Allstars','blue',9,90.00,2,1),(54,'Converse','Chuck Taylor Allstars','blue',10,90.00,2,1),(55,'Converse','Chuck Taylor Allstars','blue',11,90.00,2,1),(56,'Converse','Chuck Taylor Allstars','blue',12,90.00,2,1),(57,'Converse','Chuck Taylor Allstars','white',5,90.00,2,1),(58,'Converse','Chuck Taylor Allstars','white',6,90.00,2,1),(59,'Converse','Chuck Taylor Allstars','white',7,90.00,2,1),(60,'Converse','Chuck Taylor Allstars','white',8,90.00,2,1),(61,'Converse','Chuck Taylor Allstars','white',9,90.00,2,1),(62,'Converse','Chuck Taylor Allstars','white',10,90.00,2,1),(63,'Converse','Chuck Taylor Allstars','white',11,90.00,2,1),(64,'Converse','Chuck Taylor Allstars','white',12,90.00,2,1),(65,'Vans','Old Skools','black',5,90.00,5,2),(66,'Vans','Old Skools','black',6,90.00,5,2),(67,'Vans','Old Skools','black',7,90.00,5,2),(68,'Vans','Old Skools','black',8,90.00,5,2),(69,'Vans','Old Skools','black',9,90.00,5,2),(70,'Vans','Old Skools','black',10,90.00,5,2),(71,'Vans','Old Skools','black',11,90.00,5,2),(72,'Vans','Old Skools','black',12,90.00,5,2),(73,'Vans','Old Skools','blue',5,90.00,5,2),(74,'Vans','Old Skools','blue',6,90.00,5,2),(75,'Vans','Old Skools','blue',7,90.00,5,2),(76,'Vans','Old Skools','blue',8,90.00,5,2),(77,'Vans','Old Skools','blue',9,90.00,5,2),(78,'Vans','Old Skools','blue',10,90.00,5,2),(79,'Vans','Old Skools','blue',11,90.00,5,2),(80,'Vans','Old Skools','blue',12,90.00,5,2),(81,'Vans','Old Skools','white',5,90.00,5,2),(82,'Vans','Old Skools','white',6,90.00,5,2),(83,'Vans','Old Skools','white',7,90.00,5,2),(84,'Vans','Old Skools','white',8,90.00,5,2),(85,'Vans','Old Skools','white',9,90.00,5,2),(86,'Vans','Old Skools','white',10,90.00,5,2),(87,'Vans','Old Skools','white',11,90.00,5,2),(88,'Vans','Old Skools','white',12,90.00,5,2);
/*!40000 ALTER TABLE `shoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userID` int unsigned NOT NULL AUTO_INCREMENT,
  `userName` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `firstName` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `lastName` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `emailAddress` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `address` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `city` varchar(45) COLLATE utf8_bin DEFAULT NULL,
  `state` varchar(2) COLLATE utf8_bin DEFAULT NULL,
  `zipCode` varchar(5) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'test_user','bf400c2a1cbc2c5536aec42018864edb5738ed69bf5488a017a1aead21f888ae05a13c2f30de004a4a6fa4eedeb8c8d62f79712a4f8489e7eca408e57b36c250','John','Doe','test_user@email.com','123 Fake Street','San Diego','CA','92810'),(3,'test_user2','6e784ee231562819f1c01968c08db395a17470b44594314804b2358ef448f783a1aba2a4be16529be1e80ba6f310f6881738c1cc6c7790e6652dd9cd94d25a56','Jane','Deer','test_user2@email.com','45678 Imaginary Road, Unit 13','San Diego','CA','92182'),(8,'test_user3','bf400c2a1cbc2c5536aec42018864edb5738ed69bf5488a017a1aead21f888ae05a13c2f30de004a4a6fa4eedeb8c8d62f79712a4f8489e7eca408e57b36c250','Doug','Guy','test_user3@email.com','8724 Street Drive','San Diego','CA','92182'),(9,'test_user4','bf400c2a1cbc2c5536aec42018864edb5738ed69bf5488a017a1aead21f888ae05a13c2f30de004a4a6fa4eedeb8c8d62f79712a4f8489e7eca408e57b36c250','Jean','Smith','test_user4@email.com','87248 Test Court, Unit 4','La Mesa','CA','92152'),(10,'test_user6','bf400c2a1cbc2c5536aec42018864edb5738ed69bf5488a017a1aead21f888ae05a13c2f30de004a4a6fa4eedeb8c8d62f79712a4f8489e7eca408e57b36c250','Ashley','Smith','test_user6@email.com','1122 State Street','San Diego','CA','92114'),(11,'test_user7','bf400c2a1cbc2c5536aec42018864edb5738ed69bf5488a017a1aead21f888ae05a13c2f30de004a4a6fa4eedeb8c8d62f79712a4f8489e7eca408e57b36c250','Mike','Joe','test_user7@gmail.com','1234 W East Street','San Diego','CA','92134'),(12,'alirezaabdoli','e6c83b282aeb2e022844595721cc00bbda47cb24537c1779f9bb84f04039e1676e6ba8573e588da1052510e3aa0a32a9e55879ae22b0c2d62136fc0a3e85f8bb','Alireza','Abdoli','aabdoli@sdsu.edu','5500 Campanile Drive','San Diego','CA','92182');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-08 20:36:50

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
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `paymentID` int unsigned NOT NULL AUTO_INCREMENT,
  `userID` int unsigned NOT NULL,
  `cardType` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `cardNumber` varchar(16) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `cardName` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `cardSecurityNum` int unsigned NOT NULL,
  `cardExpDate` date NOT NULL,
  `cardZipcode` int NOT NULL,
  PRIMARY KEY (`paymentID`),
  KEY `userID_idx` (`userID`),
  CONSTRAINT `userID` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shoes`
--

DROP TABLE IF EXISTS `shoes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shoes` (
  `shoeID` int unsigned NOT NULL AUTO_INCREMENT,
  `shoeBrand` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `shoeColor` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `shoePrice` decimal(3,2) unsigned zerofill DEFAULT NULL,
  `shoeSize` int unsigned DEFAULT NULL,
  `stockAmount` int unsigned DEFAULT NULL,
  PRIMARY KEY (`shoeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shoes`
--

LOCK TABLES `shoes` WRITE;
/*!40000 ALTER TABLE `shoes` DISABLE KEYS */;
/*!40000 ALTER TABLE `shoes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transactionID` int unsigned NOT NULL AUTO_INCREMENT,
  `userID` int unsigned NOT NULL,
  `paymentID` int unsigned NOT NULL,
  `orderDate` date NOT NULL,
  `totalPrice` decimal(3,2) NOT NULL,
  PRIMARY KEY (`transactionID`),
  KEY `paymentID_idx` (`paymentID`),
  CONSTRAINT `paymentID` FOREIGN KEY (`paymentID`) REFERENCES `payments` (`paymentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'test_user','bf400c2a1cbc2c5536aec42018864edb5738ed69bf5488a017a1aead21f888ae05a13c2f30de004a4a6fa4eedeb8c8d62f79712a4f8489e7eca408e57b36c250','John','Doe','test_user@email.com','123 Fake Street','San Diego','CA','92810'),(3,'test_user2','6e784ee231562819f1c01968c08db395a17470b44594314804b2358ef448f783a1aba2a4be16529be1e80ba6f310f6881738c1cc6c7790e6652dd9cd94d25a56','Jane','Deer','test_user2@email.com','45678 Imaginary Road, Unit 13','San Diego','CA','92182'),(8,'test_user3','bf400c2a1cbc2c5536aec42018864edb5738ed69bf5488a017a1aead21f888ae05a13c2f30de004a4a6fa4eedeb8c8d62f79712a4f8489e7eca408e57b36c250','Doug','Guy','test_user3@email.com','8724 Street Drive','San Diego','CA','92182'),(9,'test_user4','bf400c2a1cbc2c5536aec42018864edb5738ed69bf5488a017a1aead21f888ae05a13c2f30de004a4a6fa4eedeb8c8d62f79712a4f8489e7eca408e57b36c250','Jean','Smith','test_user4@email.com','87248 Test Court, Unit 4','La Mesa','CA','92152');
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

-- Dump completed on 2021-11-03 18:27:09

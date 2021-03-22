-- MySQL dump 10.13  Distrib 8.0.22, for macos10.15 (x86_64)
--
-- Host: localhost    Database: apidb
-- ------------------------------------------------------
-- Server version	8.0.22

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
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (2,'José Antunes','Matematica Aplicada',NULL,'<h1>Lorem Ipsum</h1>\r\n\r\n<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. In rutrum sodales viverra. Donec sodales laoreet suscipit. Morbi pellentesque non quam eu tempor. Integer vehicula semper ligula sit amet tincidunt. Curabitur id ligula dui. Phasellus vitae congue massa, sed luctus ex.&nbsp;</p>\r\n','2:00','R$ 45,00',NULL),(4,'Sonia Valente','Portugues Redação',NULL,'<p>teste mesmo sendo teste &eacute; apenas um teste</p>\r\n','1:00','R$ 22:00',NULL);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (1,'Roberto Dias','roberto','robertott@gmail.com','25/12/1995','05133000','11989336521','Rua da Paixão, 35','Sao Paulo','student','Cartão Visa','44421547854','123456',NULL,NULL),(3,'Juliana Mattos','juliana','julianass@gmail.com','10/09/2000','02995000','21954752211','Avenida do estado, 778','Rio de Janeiro','teacher','Null','31084421422','$5$rounds=535000$oz9IkEEzlg9vEAdR$jdLIJ3GhyZT5XSyg8uLWz7bPIaUoJpjRZGIRjDcXI5.',NULL,NULL),(4,'Sandro Silva Sousa','sandro','sandrosil@gmail.com','16/05/1999','01225400','31963255444','Rua das flores, 154','Belo Horizonte','student','nuncamais','04215447775','$5$rounds=535000$oz9IkEEzlg9vEAdR$jdLIJ3GhyZT5XSyg8uLWz7bPIaUoJpjRZGIRjDcXI5.',NULL,NULL);
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'wilton','wilton@gmail.com','wilton','$5$rounds=535000$dOztrRh8keYoZ5dV$G2su2sP5lK6xeBJ0mgHdWc0Dtu9/6dgVQDvR/8j8WD5');
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

-- Dump completed on 2021-03-21 21:19:15

-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: barn
-- ------------------------------------------------------
-- Server version	5.7.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(255) NOT NULL,
  `camera` varchar(255) NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (1,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/03/43[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:03:43'),(2,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/03/49[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:03:49'),(3,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/03/55[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:03:55'),(4,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/03/58[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:03:58'),(5,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/04[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:04'),(6,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/07[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:07'),(7,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/10[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:10'),(8,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/16[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:16'),(9,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/19[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:19'),(10,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/23[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:23'),(11,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/29[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:29'),(12,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/41[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:41'),(13,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/47[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:47'),(14,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/04/56[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:04:56'),(15,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/05/44[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:05:44'),(16,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/06/58[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:06:58'),(17,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/07/44[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:07:44'),(18,'/Barn/5C033BCPAGBC9CE/2019-10-18/001/jpg/13/08/06[M][0@0][0].jpg','5C033BCPAGBC9CE','2019-10-18 16:08:06');
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recognition`
--

DROP TABLE IF EXISTS `recognition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recognition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `normal_situation` float NOT NULL,
  `aggression_frontal` float NOT NULL,
  `aggression_lateral` float NOT NULL,
  `aggression_vertical` float NOT NULL,
  `aggression_overtaking` float NOT NULL,
  `curiosity` float NOT NULL,
  `queuing_fewer` float NOT NULL,
  `queuing_crowded` float NOT NULL,
  `drinking_water` float NOT NULL,
  `low_visibility` float NOT NULL,
  `image_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `image_id` (`image_id`),
  CONSTRAINT `recognition_ibfk_1` FOREIGN KEY (`image_id`) REFERENCES `image` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recognition`
--

LOCK TABLES `recognition` WRITE;
/*!40000 ALTER TABLE `recognition` DISABLE KEYS */;
INSERT INTO `recognition` VALUES (1,0,0,1,0,0,0,0,1.36062e-20,0,0,1),(2,0,0,0,0,0,0,0,1,0,0,2),(3,0,0,0,0,0,1,0,3.12336e-21,0,0,3),(4,0.00000000000681217,0,0,0,0,6.70022e-31,0,1,0,0,4),(5,0,0,0,0,0,0.00000000233232,1,8.18484e-36,0,0,5),(6,0,0,0,0,0,1,0,0,0,0,6),(7,0,0,0,0,0,0,1,6.23966e-21,0,0,7),(8,0,0,0,0,0,0,0,1,0,0,8),(9,0,0,1,0,0,2.88102e-30,1.84455e-23,3.59372e-32,0,0,9),(10,0,0,7.92818e-29,0,0,1.37173e-26,4.72997e-33,1,0,0,10),(11,0,0,0,0,0,1,0.0000000182423,0.00000000000540229,0,0,11),(12,0,0,0,0,0,0.318265,0.681735,1.52505e-26,0,0,12),(13,0,0,0,0,0,1,1.82375e-28,2.42997e-33,0,0,13),(14,0,0,0,0,0,1,0.00000000000039466,0,0,0,14),(15,0,0,0,0,0,1,8.75671e-34,0,0,0,15),(16,0,0,0,0,0,1,0.000000000830439,0.0000000000000291258,0,0,16),(17,0,0,0,0,0,1,1.54171e-28,0,0,0,17),(18,0,0,0,0,0,0.000000000341224,1,0,0,0,18);
/*!40000 ALTER TABLE `recognition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `segmentation`
--

DROP TABLE IF EXISTS `segmentation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `segmentation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_milking` tinyint(1) NOT NULL,
  `distance_array` varchar(255) NOT NULL,
  `n_cows` int(11) NOT NULL,
  `n_humans` int(11) NOT NULL,
  `image_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `image_id` (`image_id`),
  CONSTRAINT `segmentation_ibfk_1` FOREIGN KEY (`image_id`) REFERENCES `image` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `segmentation`
--

LOCK TABLES `segmentation` WRITE;
/*!40000 ALTER TABLE `segmentation` DISABLE KEYS */;
INSERT INTO `segmentation` VALUES (1,0,'[inf]',1,0,17),(2,0,'[inf]',1,0,18);
/*!40000 ALTER TABLE `segmentation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'barn'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-18 13:08:29

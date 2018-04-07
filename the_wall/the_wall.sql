CREATE DATABASE  IF NOT EXISTS `the_wall` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `the_wall`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: the_wall
-- ------------------------------------------------------
-- Server version	5.7.18-log

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
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `message_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comments_users1_idx` (`user_id`),
  KEY `fk_comments_messages1_idx` (`message_id`),
  CONSTRAINT `fk_comments_messages1` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (1,'This is the first comment!!! This is the first comment!!! This is the first comment!!! This is the first comment!!! ','2018-04-03 13:43:59','2018-04-03 13:43:59',5,4),(2,'Second comment!!! Second comment!!! Second comment!!! Second comment!!! Second comment!!! Second comment!!! ','2018-04-03 14:12:52','2018-04-03 14:12:52',5,4),(3,'No Pablo, NO! No Pablo, NO! No Pablo, NO! No Pablo, NO! No Pablo, NO! No Pablo, NO! No Pablo, NO! ','2018-04-03 14:17:23','2018-04-03 14:17:23',1,5),(4,'REPLYING TO MY OWN MESSAGE!!!','2018-04-03 14:18:21','2018-04-03 14:18:21',1,6),(5,'AND AGAIN!','2018-04-03 14:18:29','2018-04-03 14:18:29',1,6),(6,'Nyan~~~!','2018-04-03 14:43:06','2018-04-03 14:43:06',1,5),(7,'LAST TEST!','2018-04-03 14:43:24','2018-04-03 14:43:24',1,3);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_messages_users_idx` (`user_id`),
  CONSTRAINT `fk_messages_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (3,'Second message!!! Second message!!! Second message!!! Second message!!! Second message!!! Second message!!! Second message!!! Second message!!! Second message!!! Second message!!! Second message!!! Second message!!!','2018-04-03 11:11:08','2018-04-03 11:11:08',1),(4,'Third message!!! Third message!!! Third message!!! Third message!!! Third message!!! Third message!!! Third message!!! Third message!!! Third message!!! Third message!!! Third message!!! Third message!!! Third message!!!','2018-04-03 11:11:29','2018-04-03 11:11:29',1),(5,'Fourth message!!! Fourth message!!! Fourth message!!! Fourth message!!! Fourth message!!! Fourth message!!! Fourth message!!! Fourth message!!! Fourth message!!! Fourth message!!!','2018-04-03 11:46:47','2018-04-03 11:46:47',5),(6,'THIS IS THE LAST MESSAGE! THIS IS THE LAST MESSAGE! THIS IS THE LAST MESSAGE! THIS IS THE LAST MESSAGE! ','2018-04-03 14:18:11','2018-04-03 14:18:11',1);
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `salt` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Gerardo','Blanco','filoblanco@yahoo.com','ab60c614c810297bce386d5110bf0043','7926296fa01e4c873c84484c64dfd4','2018-04-02 23:04:30','2018-04-02 23:04:30'),(5,'Pablo','Jinesta','123@123.com','6e9a84a8c0dd5dad2e76678f34f05be7','9f908a2a1bed433f6103d1277c59bb','2018-04-03 11:46:18','2018-04-03 11:46:18');
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

-- Dump completed on 2018-04-03 14:48:03

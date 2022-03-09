CREATE DATABASE d0020e_dev;
use database d0020e_dev;



DROP TABLE IF EXISTS `monitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monitor` (
  `monitorID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`monitorID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monitor`
--

LOCK TABLES `monitor` WRITE;
/*!40000 ALTER TABLE `monitor` DISABLE KEYS */;
INSERT INTO `monitor` VALUES (4,'Home1'),(5,'Home2'),(6,'Home3');
/*!40000 ALTER TABLE `monitor` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `role` varchar(128) NOT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (4,'1','1','client1','client'),(5,'2','2','client2','client'),(6,'3','3','client3','client'),(7,'patrik','$2b$14$PwBK4Zh7TJ8ZniYEjVkBq.L8Dp3CQlX6Q/h7L3udHGWmZQHVLgW5O','client','user');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subscription` (
  `subID` int NOT NULL AUTO_INCREMENT,
  `userID` int NOT NULL,
  `monitorID` int NOT NULL,
  PRIMARY KEY (`subID`),
  UNIQUE KEY `uc_user_monitor` (`userID`,`monitorID`),
  KEY `monitorID` (`monitorID`),
  CONSTRAINT `subscription_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`),
  CONSTRAINT `subscription_ibfk_2` FOREIGN KEY (`monitorID`) REFERENCES `monitor` (`monitorID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscription`
--

LOCK TABLES `subscription` WRITE;
/*!40000 ALTER TABLE `subscription` DISABLE KEYS */;
INSERT INTO `subscription` VALUES (1,4,4),(2,5,4),(3,6,4),(7,6,5),(4,7,4),(5,7,5),(9,7,6);
/*!40000 ALTER TABLE `subscription` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `actiontype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actiontype` (
  `actionTypeID` int NOT NULL AUTO_INCREMENT,
  `nameType` varchar(128) NOT NULL,
  PRIMARY KEY (`actionTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actiontype`
--

LOCK TABLES `actiontype` WRITE;
/*!40000 ALTER TABLE `actiontype` DISABLE KEYS */;
INSERT INTO `actiontype` VALUES (1,'read'),(2,'solved');
/*!40000 ALTER TABLE `actiontype` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;


DROP TABLE IF EXISTS `alarmtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alarmtype` (
  `alarmTypeID` int NOT NULL AUTO_INCREMENT,
  `nameType` varchar(128) NOT NULL,
  PRIMARY KEY (`alarmTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarmtype`
--

LOCK TABLES `alarmtype` WRITE;
/*!40000 ALTER TABLE `alarmtype` DISABLE KEYS */;
INSERT INTO `alarmtype` VALUES (1,'fall_detected'),(2,'fall_confirmed');
/*!40000 ALTER TABLE `alarmtype` ENABLE KEYS */;
UNLOCK TABLES;


DROP TABLE IF EXISTS `alarm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alarm` (
  `alarmID` int NOT NULL AUTO_INCREMENT,
  `monitorID` int NOT NULL,
  `alarmType` int NOT NULL,
  `read` int NOT NULL,
  `resolved` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`alarmID`),
  KEY `fk4` (`monitorID`),
  KEY `fk5` (`alarmType`),
  CONSTRAINT `fk4` FOREIGN KEY (`monitorID`) REFERENCES `monitor` (`monitorID`),
  CONSTRAINT `fk5` FOREIGN KEY (`alarmType`) REFERENCES `alarmtype` (`alarmTypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarm`
--

LOCK TABLES `alarm` WRITE;
/*!40000 ALTER TABLE `alarm` DISABLE KEYS */;
INSERT INTO `alarm` VALUES (27,4,1,1,1,'2022-03-09 01:27:23'),(28,4,1,0,0,'2022-02-24 15:41:13'),(29,4,1,0,0,'2022-02-24 15:43:57'),(30,4,1,0,1,'2022-03-09 01:45:08'),(31,4,1,0,0,'2022-02-24 15:48:02'),(32,4,2,0,0,'2022-02-24 15:48:02'),(33,4,1,0,0,'2022-02-24 16:05:37'),(34,4,1,0,0,'2022-02-24 16:09:19'),(35,4,2,0,0,'2022-02-24 16:09:19'),(36,4,1,0,0,'2022-02-24 16:12:56'),(37,4,1,0,0,'2022-02-24 16:16:34'),(38,4,2,0,0,'2022-02-24 16:16:34'),(39,4,1,0,0,'2022-02-24 16:26:36'),(40,4,1,0,0,'2022-02-24 16:28:35'),(41,4,2,0,0,'2022-02-24 16:28:35'),(42,4,1,0,0,'2022-02-24 16:32:58'),(43,4,2,0,0,'2022-02-24 16:32:58'),(44,4,1,0,0,'2022-02-24 16:35:12'),(45,4,1,0,0,'2022-02-24 16:39:07'),(46,4,2,0,0,'2022-02-24 16:39:07'),(47,4,1,0,0,'2022-02-24 16:39:48'),(48,4,1,0,0,'2022-02-24 16:40:15'),(49,4,1,0,0,'2022-02-24 16:40:42'),(50,4,1,0,0,'2022-02-24 16:42:37'),(51,4,1,0,0,'2022-02-24 16:43:19'),(52,4,2,0,0,'2022-02-24 16:43:19'),(53,4,1,0,0,'2022-02-24 17:09:47'),(54,4,2,0,0,'2022-02-24 17:09:47'),(55,4,1,0,0,'2022-02-24 17:10:18'),(56,4,1,0,0,'2022-02-24 17:10:27'),(57,4,2,0,0,'2022-02-24 17:10:27'),(58,4,1,0,0,'2022-02-24 17:13:48'),(59,4,2,0,0,'2022-02-24 17:13:48'),(60,4,2,0,0,'2022-03-07 16:02:34'),(61,4,2,0,0,'2022-03-07 16:02:34'),(62,4,2,0,0,'2022-03-07 16:02:34'),(63,4,2,0,0,'2022-03-07 16:02:34'),(64,4,2,0,0,'2022-03-07 16:02:34'),(65,4,2,0,0,'2022-03-07 16:02:34'),(66,4,2,0,0,'2022-03-07 16:02:34'),(67,4,2,0,0,'2022-03-07 16:02:34'),(68,4,2,0,0,'2022-03-07 16:02:34'),(69,4,2,0,0,'2022-03-07 16:02:34'),(70,4,2,0,0,'2022-03-07 16:02:34'),(71,4,2,0,0,'2022-03-07 16:02:34'),(72,4,2,0,0,'2022-03-07 16:02:34'),(73,4,2,0,0,'2022-03-07 16:02:34'),(74,4,2,0,0,'2022-03-07 16:02:34'),(75,4,2,0,0,'2022-03-07 16:02:34'),(76,4,2,0,0,'2022-03-07 16:02:34'),(77,4,2,0,0,'2022-03-07 16:02:34'),(78,4,2,0,0,'2022-03-07 16:02:34'),(79,4,2,0,0,'2022-03-07 16:02:34'),(80,4,2,0,0,'2022-03-07 16:02:34'),(81,4,2,0,0,'2022-03-07 16:02:34'),(82,4,2,0,0,'2022-03-07 16:02:34'),(83,4,2,0,0,'2022-03-07 16:02:34'),(84,4,2,0,0,'2022-03-07 16:02:34'),(85,4,2,0,0,'2022-03-07 16:02:34'),(86,4,2,0,0,'2022-03-07 16:02:34'),(87,4,2,0,0,'2022-03-07 16:02:34'),(88,4,2,0,0,'2022-03-07 16:02:34'),(89,4,2,0,0,'2022-03-07 16:02:34'),(90,4,2,0,0,'2022-03-07 16:02:34'),(91,4,2,0,0,'2022-03-07 16:02:34'),(92,4,2,0,0,'2022-03-07 16:02:34'),(93,4,2,0,0,'2022-03-07 16:02:34'),(94,4,2,0,0,'2022-03-07 16:02:34'),(95,4,2,0,0,'2022-03-07 16:02:34'),(96,4,2,0,0,'2022-03-07 16:02:34'),(97,4,2,0,0,'2022-03-07 16:02:34'),(98,4,2,0,0,'2022-03-07 16:02:34'),(99,4,2,0,0,'2022-03-07 16:02:34'),(100,4,2,0,0,'2022-03-07 16:02:34'),(101,4,2,0,0,'2022-03-07 16:02:34'),(102,4,2,0,0,'2022-03-07 16:02:34'),(103,4,2,0,0,'2022-03-07 16:02:34'),(104,4,2,0,0,'2022-03-07 16:02:34'),(105,4,2,0,0,'2022-03-07 16:02:34'),(106,4,2,0,0,'2022-03-07 16:02:34'),(107,4,2,0,0,'2022-03-07 16:02:34'),(108,4,2,0,0,'2022-03-07 16:02:34'),(109,4,2,0,0,'2022-03-07 16:02:34'),(110,4,1,0,0,'2022-03-09 11:30:25'),(111,4,2,0,0,'2022-03-09 11:30:25'),(112,4,1,0,0,'2022-03-09 11:31:01'),(113,4,2,0,0,'2022-03-09 11:31:01'),(114,4,1,0,0,'2022-03-09 11:43:02'),(115,4,2,0,0,'2022-03-09 11:43:02'),(116,4,1,0,0,'2022-03-09 11:48:48'),(117,4,1,0,0,'2022-03-09 11:49:40'),(118,4,2,0,0,'2022-03-09 11:49:40'),(119,4,1,0,0,'2022-03-09 12:01:04'),(120,4,2,0,0,'2022-03-09 12:01:04'),(121,4,1,0,0,'2022-03-09 12:01:47'),(122,4,2,0,0,'2022-03-09 12:01:47'),(123,4,1,0,0,'2022-03-09 12:03:35'),(124,4,2,0,0,'2022-03-09 12:03:35'),(125,4,1,0,0,'2022-03-09 12:04:05'),(126,4,2,0,0,'2022-03-09 12:04:05'),(127,4,1,0,0,'2022-03-09 12:06:12'),(128,4,2,0,0,'2022-03-09 12:06:12'),(129,4,1,0,0,'2022-03-09 12:06:47'),(130,4,2,0,0,'2022-03-09 12:06:47'),(131,4,1,0,0,'2022-03-09 12:07:56'),(132,4,2,0,0,'2022-03-09 12:07:56'),(133,4,1,0,0,'2022-03-09 12:08:27'),(134,4,1,0,0,'2022-03-09 12:14:34'),(135,4,2,0,0,'2022-03-09 12:14:34'),(136,4,1,0,0,'2022-03-09 12:29:25'),(137,4,2,0,0,'2022-03-09 12:29:25'),(138,4,1,0,0,'2022-03-09 12:33:07'),(139,4,2,0,0,'2022-03-09 12:33:07'),(140,4,1,0,0,'2022-03-09 12:34:10'),(141,4,2,0,0,'2022-03-09 12:34:10'),(142,4,1,0,0,'2022-03-09 12:34:39'),(143,4,1,0,0,'2022-03-09 12:38:29');
/*!40000 ALTER TABLE `alarm` ENABLE KEYS */;
UNLOCK TABLES;



--
-- Table structure for table `action`
--

DROP TABLE IF EXISTS `action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `action` (
  `userID` int NOT NULL,
  `alarmID` int NOT NULL,
  `actionType` int NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`userID`,`alarmID`,`actionType`),
  KEY `fk7` (`alarmID`),
  KEY `fk8` (`actionType`),
  CONSTRAINT `fk6` FOREIGN KEY (`userID`) REFERENCES `user` (`userID`),
  CONSTRAINT `fk7` FOREIGN KEY (`alarmID`) REFERENCES `alarm` (`alarmID`),
  CONSTRAINT `fk8` FOREIGN KEY (`actionType`) REFERENCES `actiontype` (`actionTypeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action`
--

LOCK TABLES `action` WRITE;
/*!40000 ALTER TABLE `action` DISABLE KEYS */;
INSERT INTO `action` VALUES (7,27,1,'2022-03-08 17:09:32'),(7,27,2,'2022-03-08 17:09:32'),(7,30,2,'2022-03-08 17:09:32');
/*!40000 ALTER TABLE `action` ENABLE KEYS */;
UNLOCK TABLES;






DROP TABLE IF EXISTS `sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor` (
  `sensorID` int NOT NULL AUTO_INCREMENT,
  `monitorID` int NOT NULL,
  `deviceID` varchar(64) NOT NULL,
  PRIMARY KEY (`sensorID`),
  KEY `fk1` (`monitorID`),
  CONSTRAINT `fk1` FOREIGN KEY (`monitorID`) REFERENCES `monitor` (`monitorID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor`
--

LOCK TABLES `sensor` WRITE;
/*!40000 ALTER TABLE `sensor` DISABLE KEYS */;
INSERT INTO `sensor` VALUES (6,4,'67BA3CF4E0622323'),(7,4,'8F44CDEF5DC36678'),(8,4,'F1587D88122BE247');
/*!40000 ALTER TABLE `sensor` ENABLE KEYS */;
UNLOCK TABLES;



DROP TABLE IF EXISTS `serveraccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `serveraccess` (
  `clientID` int NOT NULL,
  `timestamp` timestamp NOT NULL,
  `token` char(64) NOT NULL,
  PRIMARY KEY (`clientID`),
  CONSTRAINT `serveraccess_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `user` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serveraccess`
--

LOCK TABLES `serveraccess` WRITE;
/*!40000 ALTER TABLE `serveraccess` DISABLE KEYS */;
INSERT INTO `serveraccess` VALUES (7,'2022-03-09 12:28:03','aeb7e2616a768c336c2ed14b1fbc1db06dfab24dfd50d6f0bb8690581cffa714');
/*!40000 ALTER TABLE `serveraccess` ENABLE KEYS */;
UNLOCK TABLES;






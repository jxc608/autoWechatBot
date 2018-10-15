-- MySQL dump 10.14  Distrib 5.5.60-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: auto_accounting
-- ------------------------------------------------------
-- Server version	5.5.60-MariaDB

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
-- Table structure for table `DServerAPP_cdkey`
--

DROP TABLE IF EXISTS `DServerAPP_cdkey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DServerAPP_cdkey` (
  `cdkey` varchar(50) NOT NULL DEFAULT '',
  `key_type` tinyint(4) DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`cdkey`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DServerAPP_cdkey`
--

LOCK TABLES `DServerAPP_cdkey` WRITE;
/*!40000 ALTER TABLE `DServerAPP_cdkey` DISABLE KEYS */;
INSERT INTO `DServerAPP_cdkey` VALUES ('3bab6334',1,0,1539314628),('3bac7bde',1,1,1539314628),('3bace790',1,0,1539314628),('3bad4ca8',1,1,1539314628),('3badb13e',1,0,1539314628),('3bae12be',1,1,1539314628),('3bb0895e',1,0,1539314628),('3bb1053c',1,1,1539314628),('3bb1727e',1,1,1539314628),('3bb1d0c0',1,0,1539314628),('3eb1829c',1,0,1539437469),('3eb28e4e',1,0,1539437469),('3eb33c72',1,0,1539437469),('3eb3c0ca',1,0,1539437469),('3eb444aa',1,0,1539437469),('3eb4b8a4',1,0,1539437469),('3eb52e10',1,0,1539437469),('3eb5adf4',1,0,1539437469),('3eb65baa',1,0,1539437469),('3eb6dd8c',1,0,1539437469),('453ccb50',1,0,1539333542),('453eb528',1,0,1539333542),('453f3944',1,0,1539333542),('453fb0cc',1,0,1539333542),('45402ee4',1,0,1539333542),('4540a3f6',1,0,1539333542),('45411732',1,0,1539333542),('45419478',1,0,1539333542),('4542151a',1,0,1539333542),('45429de6',1,0,1539333542),('495367ce',2,0,1539437487),('49542c4a',2,0,1539437487),('4954c2ae',2,0,1539437487),('49553d4c',2,0,1539437487),('4955b268',2,0,1539437487),('49562ce8',2,0,1539437487),('4956a394',2,0,1539437487),('49571a9a',2,0,1539437487),('4957af14',2,0,1539437487),('495831e6',2,0,1539437487),('4bf109c4',1,0,1539314655),('4bf22d22',1,0,1539314655),('4bf2bf44',1,0,1539314655),('4bf3364a',1,0,1539314655),('4bf3aff8',1,0,1539314655),('4bf427da',1,0,1539314655),('4bf49a62',1,0,1539314655),('4bf5309e',1,0,1539314655),('4bf5aa92',1,0,1539314655),('4bf61ff4',1,0,1539314655),('4bf6a7b2',1,0,1539314655),('4bf72502',1,0,1539314655),('4bf7a4be',1,0,1539314655),('4bf813ea',1,0,1539314655),('4bf983ce',1,0,1539314655),('4bfa1bf4',1,0,1539314655),('4bfaa326',1,0,1539314655),('4bfb1054',1,0,1539314655),('4bfb861a',1,0,1539314655),('4bfbfab4',1,0,1539314655),('4bfd306e',1,0,1539314655),('4bfdb7e6',1,0,1539314655),('4bfe2f00',1,0,1539314655),('4bfe9832',1,0,1539314655),('4bff022c',1,0,1539314655),('4bff7414',1,0,1539314655),('4bffe1c4',1,0,1539314655),('4c0060c2',1,0,1539314655),('4c00e696',1,0,1539314655),('4c015bc6',1,0,1539314655),('4c01db8c',1,0,1539314655),('4c0260b6',1,0,1539314655),('4c02d50a',1,0,1539314655),('4c034526',1,0,1539314655),('4c03baf6',1,0,1539314655),('4c042fe0',1,0,1539314655),('4c04b0c8',1,0,1539314655),('4c051b08',1,0,1539314655),('4c05a37a',1,0,1539314655),('4c062480',1,0,1539314655),('4c06976c',1,0,1539314655),('4c070cd8',1,0,1539314655),('4c077e7a',1,0,1539314655),('4c07f8be',1,0,1539314655),('4c08b006',1,0,1539314655),('4c0938d2',1,0,1539314655),('4c09bc30',1,0,1539314655),('4c0a51ea',1,0,1539314655),('4c0ada48',1,0,1539314655),('4c0b6134',1,0,1539314655),('4c0be4a6',1,0,1539314655),('4c0c49d2',1,0,1539314655),('4c0cb174',1,0,1539314655),('4c0d12e0',1,0,1539314655),('4c0d89f0',1,0,1539314655),('4c0debd4',1,0,1539314655),('4c0e4b92',1,0,1539314655),('4c0ec838',1,0,1539314655),('4c0f3c8c',1,0,1539314655),('4c0fa532',1,0,1539314655),('4c101508',1,0,1539314655),('4c10a55e',1,0,1539314655),('4c111a66',1,0,1539314655),('4c11b4d0',1,0,1539314655),('4c12426a',1,0,1539314655),('4c12c032',1,0,1539314655),('4c13309e',1,0,1539314655),('4c13a772',1,0,1539314655),('4c14230a',1,0,1539314655),('4c14ada2',1,1,1539314655),('4c152fc0',1,0,1539314655),('4c15bb34',1,0,1539314655),('4c163776',1,1,1539314655),('4c16ae04',1,0,1539314655),('4c1726fe',1,0,1539314655),('4c17a2d2',1,0,1539314655),('4c1827c0',1,0,1539314655),('4c189c8c',1,0,1539314655),('4c1920e4',1,0,1539314655),('4c19a096',1,0,1539314655),('4c1a22aa',1,0,1539314655),('4c1a9b86',1,0,1539314655),('4c1b0896',1,1,1539314655),('4c1b85aa',1,0,1539314655),('4c1befae',1,0,1539314655),('4c1cb6fa',1,0,1539314655),('4c1d3468',1,0,1539314655),('4c1ddb70',1,0,1539314655),('4c1e727e',1,0,1539314655),('4c1f1b98',1,0,1539314655),('4c1fa28e',1,0,1539314655),('4c203154',1,0,1539314655),('4c20a86e',1,0,1539314655),('4c211524',1,0,1539314655),('4c2181f8',1,0,1539314655),('4c21f584',1,0,1539314655),('4c225844',1,0,1539314655),('4c22d008',1,0,1539314655),('4c233714',1,0,1539314655),('4c23aec4',1,0,1539314655),('590868d6',1,0,1539325844),('59096ba0',1,0,1539325844),('5909f390',1,0,1539325844),('590a72ca',1,0,1539325844),('590b09ce',1,0,1539325844),('590ba2b2',1,0,1539325844),('590c26a6',1,0,1539325844),('590ca572',1,0,1539325844),('590d32bc',1,0,1539325844),('59103ffc',1,0,1539325844),('6f5f06be',2,0,1539325022),('6f5fcc2a',2,0,1539325022),('6f605ff0',2,1,1539325022),('6f60e538',2,0,1539325022),('6f616530',2,0,1539325022),('6f61dc5e',2,0,1539325022),('6f6252e2',2,0,1539325022),('6f62ce98',2,0,1539325022),('6f634698',2,0,1539325022),('6f63c154',2,0,1539325022),('7cc6ddd6',3,0,1539325045),('7cc79686',3,0,1539325045),('7cc81c46',3,1,1539325045),('7cc89950',3,1,1539325045),('7cc918b2',3,0,1539325045),('7cc98f04',3,0,1539325045),('7cca0682',3,1,1539325045),('7cca9994',3,0,1539325045),('7ccb1090',3,0,1539325045),('7ccb92c2',3,0,1539325045),('ba077718',1,0,1539574685),('ba0818ee',1,0,1539574685),('ba088ca2',1,0,1539574685),('ba091708',1,0,1539574685),('ba098fd0',1,0,1539574685),('ba0cc6a0',1,0,1539574685),('ba0d4eae',1,0,1539574685),('ba0ddd06',1,0,1539574685),('ba0e600a',1,0,1539574685),('ba0ee9d0',1,0,1539574685);
/*!40000 ALTER TABLE `DServerAPP_cdkey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DServerAPP_choice`
--

DROP TABLE IF EXISTS `DServerAPP_choice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DServerAPP_choice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `choice_text` varchar(200) NOT NULL,
  `votes` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DServerAPP_choice_question_id_56e4b483_fk_DServerAPP_question_id` (`question_id`),
  CONSTRAINT `DServerAPP_choice_question_id_56e4b483_fk_DServerAPP_question_id` FOREIGN KEY (`question_id`) REFERENCES `DServerAPP_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DServerAPP_choice`
--

LOCK TABLES `DServerAPP_choice` WRITE;
/*!40000 ALTER TABLE `DServerAPP_choice` DISABLE KEYS */;
/*!40000 ALTER TABLE `DServerAPP_choice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DServerAPP_clubs`
--

DROP TABLE IF EXISTS `DServerAPP_clubs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DServerAPP_clubs` (
  `uuid` char(32) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `expired_time` decimal(19,6) NOT NULL,
  `cost_mode` int(11) NOT NULL,
  `cost_param` varchar(200) NOT NULL,
  `profit` int(11) NOT NULL,
  PRIMARY KEY (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DServerAPP_clubs`
--

LOCK TABLES `DServerAPP_clubs` WRITE;
/*!40000 ALTER TABLE `DServerAPP_clubs` DISABLE KEYS */;
INSERT INTO `DServerAPP_clubs` VALUES ('057ec860cd1411e8acea525400bb9a83','qudao','clear123',1541925577.357132,0,'none',0),('6c10d01ccb9011e88e0d525400bb9a83','nathan123','12345',1539068178.357081,1,'10',0),('7cf6be1cbf0111e881a63497f629cee7','18811333964','34weah324n',1540279525.197402,0,'none',0),('abbd86f4beff11e8b1773497f629cee7','balana608','18811333964',1537686594.206284,0,'none',0);
/*!40000 ALTER TABLE `DServerAPP_clubs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DServerAPP_gameid`
--

DROP TABLE IF EXISTS `DServerAPP_gameid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DServerAPP_gameid` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_nick_name` varchar(2000) DEFAULT NULL,
  `gameid` varchar(20) CHARACTER SET latin1 NOT NULL,
  `player_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DServerAPP_gameid_player_id_3bc460dc_fk_DServerAPP_player_id` (`player_id`),
  CONSTRAINT `DServerAPP_gameid_player_id_3bc460dc_fk_DServerAPP_player_id` FOREIGN KEY (`player_id`) REFERENCES `DServerAPP_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DServerAPP_gameid`
--

LOCK TABLES `DServerAPP_gameid` WRITE;
/*!40000 ALTER TABLE `DServerAPP_gameid` DISABLE KEYS */;
INSERT INTO `DServerAPP_gameid` VALUES (1,'?','251566',2),(2,'??','299358',29),(4,'??xxx','179754',30),(5,'??','496687',31),(6,'??','387464',32),(7,'wbh','10784',33),(8,'????','429580',34),(9,'Mr.?','326710',35),(10,'b\'\\xf0\\x9f\\x8c\\xb9\'','637665',21),(11,'b\'\\xe4\\xb8\\xa5\\xe5\\xbb\\xb6\\xe8\\xb4\\xb5\'','550839',22),(12,'b\'\\xe5\\x8a\\x9d\\xe5\\x90\\x9b\'','557419',72),(13,'b\'\\xe6\\x94\\xbe\\xe7\\xba\\xb5\'','451835',23),(14,'b\'\\xe5\\x8f\\xb6\\xe5\\xad\\x90\'','540000',36),(15,'b\'\\xe3\\x80\\x82\'','350478',37),(16,'b\'\\xe5\\xbf\\x83\\xe5\\x93\\xa5\'','387616',38),(17,'b\'\\xe6\\x83\\x85\\xe8\\xb0\\x8a\'','415598',39),(18,'b\'\\xe9\\x99\\x88\\xe7\\x81\\xbf\\xe4\\xbb\\x81\'','370886',40),(19,'b\'\\xe9\\xbe\\x99\\xe8\\xa1\\x8c\\xe5\\xa4\\xa9\\xe4\\xb8\\x8b\'','357712',41),(20,'b\'\\xe5\\xa4\\x95\\xe9\\x98\\xb3\'','596618',42),(21,'b\'\\xef\\xbc\\x81\\xef\\xbc\\x81\'','170281',43),(22,'b\'^_^\\xe7\\xa6\\x8f\'','637115',44),(23,'b\'\\xe5\\xa3\\xb9=\\xe5\\xa3\\xb9\'','249591',45),(24,'b\'\\xe9\\x8e\\x8f\\xe7\\x85\\x8c\'','624713',46),(25,'b\'rose\'','22583',47),(26,'b\'\\xe4\\xbd\\xa0\\xe7\\x9a\\x84\\xe5\\x90\\x8d\\xe5\\xad\\x97\'','421027',48),(27,'b\'\\xe6\\x96\\x8c\\xe6\\x96\\x8c\'','218525',49),(28,'b\'.\'','243636',50),(29,'b\'casual\'','170219',51),(30,'b\'\\xe8\\xbf\\x87\\xe5\\xbe\\x80\'','390822',52),(31,'b\'\\xe7\\xae\\x80\\xe5\\x8d\\x95\'','299079',53),(32,'b\'\\xe5\\x8f\\x9b\\xe9\\x80\\x86\'','372566',54),(33,'b\'miki\'','640560',55),(34,'b\'ioco\\xe3\\x80\\x82\'','358411',56),(35,'b\'\\xe6\\x88\\x90\\xe6\\xb5\\xa91\'','348330',57),(36,'b\'bin\'','367460',58),(37,'b\'\\xe9\\x98\\xbf\\xe5\\xbc\\xba\'','636449',59),(38,'b\'\\xe4\\xba\\xb2\\xe4\\xba\\xb2\\xe4\\xba\\xb2\'','317900',60),(39,'b\'\\xe9\\x9d\\x92\\xe5\\xb1\\xb1\'','468312',61),(40,'b\'\\xe4\\xb8\\x8b\\xe5\\xad\\x90\\xe7\\xa7\\x92\'','498096',62),(41,'b\'\\xe9\\xa3\\x9e\\xe9\\xbe\\x99\\xe5\\x8f\\xb7\'','108135',63),(42,'b\'\\xe7\\xa6\\xb9\\xe8\\xb1\\xaa\'','132870',64),(43,'b\'aa\\xe5\\xb0\\x8f\'','491532',65),(44,'b\'\\xe5\\x9b\\xbd\\xe9\\x99\\x85\\xe7\\xad\\xbe\\xe8\\xaf\\x81\'','570529',66),(45,'b\'\\xe5\\xa4\\xa9\\xe5\\xa4\\xa9\\xe5\\xbc\\x80\\xe5\\xbf\\x83\'','606368',67),(46,'b\'\\xe5\\xb0\\x8f\\xe6\\x9e\\x97\'','491026',68),(47,'b\'\\xe9\\x99\\x8c\\xe8\\xb7\\xaf\'','636591',69),(48,'b\'\\xe4\\xbd\\x99\\xe7\\x94\\x9f\'','196586',70),(49,'b\'\\xe4\\xb8\\x89\\xe8\\x97\\x8f\'','328743',71),(50,'b\'\\xe6\\xb5\\x8b\\xe8\\xaf\\x95\\xe6\\xb8\\xb8\\xe6\\x88\\x8f\'','ceshiyouxi',73),(51,'游戏','youxi',76);
/*!40000 ALTER TABLE `DServerAPP_gameid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DServerAPP_historygame`
--

DROP TABLE IF EXISTS `DServerAPP_historygame`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DServerAPP_historygame` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` varchar(10) NOT NULL,
  `hoster_name` varchar(20) NOT NULL,
  `round_number` int(11) NOT NULL,
  `start_time` varchar(20) NOT NULL,
  `club_id` char(32) NOT NULL,
  `hoster_id` int(11) NOT NULL,
  `player_data` varchar(1000) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DServerAPP_historygame_club_id_bee2cfcd_fk_DServerAPP_clubs_uuid` (`club_id`),
  CONSTRAINT `DServerAPP_historygame_club_id_bee2cfcd_fk_DServerAPP_clubs_uuid` FOREIGN KEY (`club_id`) REFERENCES `DServerAPP_clubs` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DServerAPP_historygame`
--

LOCK TABLES `DServerAPP_historygame` WRITE;
/*!40000 ALTER TABLE `DServerAPP_historygame` DISABLE KEYS */;
INSERT INTO `DServerAPP_historygame` VALUES (1,'207592','??',10,'09-101:22','057ec860cd1411e8acea525400bb9a83',451835,'[{\"name\": \"\\u4e25\\u5ef6\\u8d35\", \"id\": 550839, \"score\": 843}, {\"name\": \"\", \"id\": 637665, \"score\": 620}, {\"name\": \"\\u529d\\u541b\\u83ab\\u6267\\u610f\", \"id\": 557419, \"score\": 250}, {\"name\": \"\\u653e\\u7eb5\", \"id\": 451835, \"score\": 230}, {\"name\": \"\", \"id\": 540000, \"score\": -267}, {\"name\": \"\", \"id\": 350478, \"score\": -347}, {\"name\": \"\\u5fc3\\u54e5\", \"id\": 387616, \"score\": -417}, {\"name\": \"\\u60c5\\u8c0a\\u3001\\u5929\\u4e0b\", \"id\": 415598, \"score\": -443}, {\"name\": \"\\u9648\\u707f\\u4ec1\", \"id\": 370886, \"score\": -469}]','2018-10-11 05:55:52.425287'),(2,'100524','??',10,'09-402:13','057ec860cd1411e8acea525400bb9a83',0,'[{\"name\": \"\", \"id\": 637665, \"score\": 1741}, {\"name\": \"\\u9f99\\u884c\\u5929\\u4e0b\", \"id\": 357712, \"score\": 733}, {\"name\": \"\\u7b80\\u5355\", \"id\": 299079, \"score\": 719}, {\"name\": \"\", \"id\": 243636, \"score\": 472}, {\"name\": \"\\u53db\\u9006\", \"id\": 372566, \"score\": 35}, {\"name\": \"\\u56e0\\u679c\", \"id\": 387464, \"score\": -166}, {\"name\": \" WBh\", \"id\": 10784, \"score\": -763}, {\"name\": \"\\u4f60\\u7684\\u540d\\u5b57\\u3002\", \"id\": 421027, \"score\": -892}, {\"name\": \"Mr\\u7fc1\", \"id\": 326710, \"score\": -1879}]','2018-10-12 07:16:26.897119'),(3,'205529','??',10,'09-318:03','057ec860cd1411e8acea525400bb9a83',0,'[{\"name\": \"\\u9752\\u5c71\", \"id\": 468312, \"score\": 6569}, {\"name\": \"\\u4e0b\\u5b50\\u79d2\", \"id\": 498096, \"score\": 121}, {\"name\": \"\\u98de\\u9f99\\u53f7\", \"id\": 108135, \"score\": 18}, {\"name\": \"\\u79b9\\u8c6a\", \"id\": 132870, \"score\": -296}, {\"name\": \"\\u5c0f\", \"id\": 491532, \"score\": -690}, {\"name\": \"\\u56fd\\u9645\\u7b7e\\u8bc1\", \"id\": 570529, \"score\": -915}, {\"name\": \"\\u5929\\u5929\\u5f00\\u5fc3\", \"id\": 606368, \"score\": -1236}, {\"name\": \"\\u5c0f\\u6797\", \"id\": 491026, \"score\": -1285}, {\"name\": \"\\u964c\\u8def\", \"id\": 636591, \"score\": -2286}]','2018-10-13 05:59:52.780028'),(4,'207592','??',10,'09-101:22','7cf6be1cbf0111e881a63497f629cee7',451835,'[{\"name\": \"\\u4e25\\u5ef6\\u8d35\", \"id\": 550839, \"score\": 843}, {\"name\": \"\", \"id\": 637665, \"score\": 620}, {\"name\": \"\\u529d\\u541b\\u83ab\\u6267\\u610f\", \"id\": 557419, \"score\": 250}, {\"name\": \"\\u653e\\u7eb5\", \"id\": 451835, \"score\": 230}, {\"name\": \"\", \"id\": 540000, \"score\": -267}, {\"name\": \"\", \"id\": 350478, \"score\": -347}, {\"name\": \"\\u5fc3\\u54e5\", \"id\": 387616, \"score\": -417}, {\"name\": \"\\u60c5\\u8c0a\\u3001\\u5929\\u4e0b\", \"id\": 415598, \"score\": -443}, {\"name\": \"\\u9648\\u707f\\u4ec1\", \"id\": 370886, \"score\": -469}]','2018-10-15 03:20:12.238644'),(5,'301395','??',10,'09-417:54','057ec860cd1411e8acea525400bb9a83',0,'[{\"name\": \"\", \"id\": 637665, \"score\": 5300}, {\"name\": \"\\u58f9=\\u58f9\", \"id\": 249591, \"score\": 769}, {\"name\": \"\\u4f60\\u7684\\u540d\\u5b57\\u3002\", \"id\": 421027, \"score\": 516}, {\"name\": \"\\u658c\\u658c\", \"id\": 218525, \"score\": 509}, {\"name\": \"\", \"id\": 243636, \"score\": -400}, {\"name\": \" WBh\", \"id\": 10784, \"score\": -1231}, {\"name\": \" I casual\", \"id\": 170219, \"score\": -1650}, {\"name\": \"\\u8fc7\\u5f80\", \"id\": 390822, \"score\": -1878}, {\"name\": \"\\u7b80\\u5355\", \"id\": 299079, \"score\": -1935}]','2018-10-15 03:53:08.070571');
/*!40000 ALTER TABLE `DServerAPP_historygame` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DServerAPP_player`
--

DROP TABLE IF EXISTS `DServerAPP_player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DServerAPP_player` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wechat_id` varchar(200) CHARACTER SET latin1 NOT NULL,
  `wechat_nick_name` varchar(2000) DEFAULT NULL,
  `club_id` char(32) CHARACTER SET latin1 NOT NULL,
  `current_score` int(11) NOT NULL,
  `history_profit` int(11) NOT NULL,
  `introducer` varchar(2000) DEFAULT NULL,
  `today_hoster_number` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DServerAPP_player_club_id_bfdfece2_fk_DServerAPP_clubs_uuid` (`club_id`),
  CONSTRAINT `DServerAPP_player_club_id_bfdfece2_fk_DServerAPP_clubs_uuid` FOREIGN KEY (`club_id`) REFERENCES `DServerAPP_clubs` (`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DServerAPP_player`
--

LOCK TABLES `DServerAPP_player` WRITE;
/*!40000 ALTER TABLE `DServerAPP_player` DISABLE KEYS */;
INSERT INTO `DServerAPP_player` VALUES (1,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(2,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(4,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(5,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(6,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(7,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(8,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(9,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(10,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(11,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(12,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(13,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(14,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(15,'','??xxx','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(16,'','AA????','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(17,'','??','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(18,'','wbh','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(19,'','????','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(20,'','Mr.?','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(21,'','b\'\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',28454,28454,'none',0),(22,'','b\'\\xe4\\xb8\\xa5\\xe5\\xbb\\xb6\\xe8\\xb4\\xb5\'','7cf6be1cbf0111e881a63497f629cee7',5901,5901,'none',0),(23,'','b\'\\xe6\\x94\\xbe\\xe7\\xba\\xb5\'','7cf6be1cbf0111e881a63497f629cee7',1610,1610,'none',0),(24,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(25,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(26,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(27,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(28,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(29,'','b\'\\xe4\\xb8\\x83\\xe5\\xad\\x90\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(30,'','b\'\\xe6\\x96\\x8c\\xe6\\x96\\x8cxxx\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(31,'','b\'AA\\xe8\\xb4\\xb7\\xe6\\xac\\xbe\\xe4\\xb8\\x93\\xe7\\xa7\\x91\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(32,'','b\'\\xe5\\x9b\\xa0\\xe6\\x9e\\x9c\'','7cf6be1cbf0111e881a63497f629cee7',-166,-166,'none',0),(33,'','b\'wbh\'','7cf6be1cbf0111e881a63497f629cee7',-5687,-5687,'none',0),(34,'','b\'\\xe4\\xb8\\x80\\xe7\\xa2\\x97\\xe9\\xa5\\xad\\xe3\\x80\\x81\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(35,'','b\'Mr.\\xe7\\xbf\\x81\'','7cf6be1cbf0111e881a63497f629cee7',-1879,-1879,'none',0),(36,'','b\'\\xe5\\x8f\\xb6\\xe5\\xad\\x90\'','7cf6be1cbf0111e881a63497f629cee7',-1869,-1869,'none',0),(37,'','b\'\\xe3\\x80\\x82\'','7cf6be1cbf0111e881a63497f629cee7',-2429,-2429,'none',0),(38,'','b\'\\xe5\\xbf\\x83\\xe5\\x93\\xa5\'','7cf6be1cbf0111e881a63497f629cee7',-2919,-2919,'none',0),(39,'','b\'\\xe6\\x83\\x85\\xe8\\xb0\\x8a\\xe3\\x80\\x81\\xe5\\xa4\\xa9\\xe4\\xb8\\x8b\'','7cf6be1cbf0111e881a63497f629cee7',-3101,-3101,'none',0),(40,'','b\'\\xe9\\x99\\x88\\xe7\\x81\\xbf\\xe4\\xbb\\x81\'','7cf6be1cbf0111e881a63497f629cee7',-3283,-3283,'none',0),(41,'','b\'\\xe9\\xbe\\x99\\xe8\\xa1\\x8c\\xe5\\xa4\\xa9\\xe4\\xb8\\x8b\'','7cf6be1cbf0111e881a63497f629cee7',733,733,'none',0),(42,'','b\'\\xe5\\xa4\\x95\\xe9\\x98\\xb3\'','7cf6be1cbf0111e881a63497f629cee7',1771,1771,'none',0),(43,'','b\'\\xef\\xbc\\x81\\xef\\xbc\\x81\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(44,'','b\'\\xf0\\x9f\\x98\\x8a\\xe7\\xa6\\x8f\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(45,'','b\'\\xe5\\xa3\\xb9=\\xe5\\xa3\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',3076,3076,'none',0),(46,'','b\'\\xe9\\x8e\\x8f\\xe7\\x85\\x8c\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(47,'','b\'rose\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(48,'','b\'\\xe4\\xbd\\xa0\\xe7\\x9a\\x84\\xe5\\x90\\x8d\\xe5\\xad\\x97\'','7cf6be1cbf0111e881a63497f629cee7',1172,1172,'none',0),(49,'','b\'\\xe6\\x96\\x8c\\xe6\\x96\\x8c\'','7cf6be1cbf0111e881a63497f629cee7',2304,2304,'none',0),(50,'','b\'.\'','7cf6be1cbf0111e881a63497f629cee7',-2063,-2063,'none',0),(51,'','b\'casual\'','7cf6be1cbf0111e881a63497f629cee7',-6600,-6600,'none',0),(52,'','b\'\\xe8\\xbf\\x87\\xe5\\xbe\\x80\'','7cf6be1cbf0111e881a63497f629cee7',-7512,-7512,'none',0),(53,'','b\'\\xe7\\xae\\x80\\xe5\\x8d\\x95\'','7cf6be1cbf0111e881a63497f629cee7',-7021,-7021,'none',0),(54,'','b\'\\xe5\\x8f\\x9b\\xe9\\x80\\x86\'','7cf6be1cbf0111e881a63497f629cee7',35,35,'none',0),(55,'','b\'miki\'','7cf6be1cbf0111e881a63497f629cee7',678,678,'none',0),(56,'','b\'ioco\\xe3\\x80\\x82\'','7cf6be1cbf0111e881a63497f629cee7',80,80,'none',0),(57,'','b\'\\xe6\\x88\\x90\\xe6\\xb5\\xa91\'','7cf6be1cbf0111e881a63497f629cee7',-150,-150,'none',0),(58,'','b\'bin\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(59,'','b\'\\xe9\\x98\\xbf\\xe5\\xbc\\xba\'','7cf6be1cbf0111e881a63497f629cee7',-2311,-2311,'none',0),(60,'','b\'\\xe4\\xba\\xb2\\xe4\\xba\\xb2\\xe4\\xba\\xb2\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(61,'','b\'\\xe9\\x9d\\x92\\xe5\\xb1\\xb1\'','7cf6be1cbf0111e881a63497f629cee7',6569,6569,'none',0),(62,'','b\'\\xe4\\xb8\\x8b\\xe5\\xad\\x90\\xe7\\xa7\\x92\'','7cf6be1cbf0111e881a63497f629cee7',121,121,'none',0),(63,'','b\'\\xe9\\xa3\\x9e\\xe9\\xbe\\x99\\xe5\\x8f\\xb7\'','7cf6be1cbf0111e881a63497f629cee7',18,18,'none',0),(64,'','b\'\\xe7\\xa6\\xb9\\xe8\\xb1\\xaa\'','7cf6be1cbf0111e881a63497f629cee7',-296,-296,'none',0),(65,'','b\'aa\\xe5\\xb0\\x8f\'','7cf6be1cbf0111e881a63497f629cee7',-690,-690,'none',0),(66,'','b\'\\xe5\\x9b\\xbd\\xe9\\x99\\x85\\xe7\\xad\\xbe\\xe8\\xaf\\x81\'','7cf6be1cbf0111e881a63497f629cee7',-915,-915,'none',0),(67,'','b\'\\xe5\\xa4\\xa9\\xe5\\xa4\\xa9\\xe5\\xbc\\x80\\xe5\\xbf\\x83\'','7cf6be1cbf0111e881a63497f629cee7',-1236,-1236,'none',0),(68,'','b\'\\xe5\\xb0\\x8f\\xe6\\x9e\\x97\'','7cf6be1cbf0111e881a63497f629cee7',-1285,-1285,'none',0),(69,'','b\'\\xe9\\x99\\x8c\\xe8\\xb7\\xaf\'','7cf6be1cbf0111e881a63497f629cee7',-2286,-2286,'none',0),(70,'','b\'\\xe4\\xbd\\x99\\xe7\\x94\\x9f\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(71,'','b\'\\xe4\\xb8\\x89\\xe8\\x97\\x8f\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(72,'','b\'\\xe5\\x8a\\x9d\\xe5\\x90\\x9b\\xe8\\x8e\\xab\\xe6\\x89\\xa7\\xe6\\x84\\x8f\'','7cf6be1cbf0111e881a63497f629cee7',1750,1750,'none',0),(73,'','b\'\\xe6\\xb5\\x8b\\xe8\\xaf\\x951\'','6c10d01ccb9011e88e0d525400bb9a83',50,0,'none',0),(74,'','b\'\\xe6\\xb5\\x8b\\xe8\\xaf\\x95\'','6c10d01ccb9011e88e0d525400bb9a83',0,0,'none',0),(75,'','测试2','6c10d01ccb9011e88e0d525400bb9a83',0,0,'none',0),(76,'','测试1','057ec860cd1411e8acea525400bb9a83',80,0,'道士',0),(77,'','指你','057ec860cd1411e8acea525400bb9a83',0,0,'none',0);
/*!40000 ALTER TABLE `DServerAPP_player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DServerAPP_question`
--

DROP TABLE IF EXISTS `DServerAPP_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DServerAPP_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_text` varchar(200) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DServerAPP_question`
--

LOCK TABLES `DServerAPP_question` WRITE;
/*!40000 ALTER TABLE `DServerAPP_question` DISABLE KEYS */;
/*!40000 ALTER TABLE `DServerAPP_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DServerAPP_score`
--

DROP TABLE IF EXISTS `DServerAPP_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DServerAPP_score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `score` int(11) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `room_id` varchar(20) NOT NULL,
  `player_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `DServerAPP_score_player_id_e83c361d_fk_DServerAPP_player_id` (`player_id`),
  CONSTRAINT `DServerAPP_score_player_id_e83c361d_fk_DServerAPP_player_id` FOREIGN KEY (`player_id`) REFERENCES `DServerAPP_player` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DServerAPP_score`
--

LOCK TABLES `DServerAPP_score` WRITE;
/*!40000 ALTER TABLE `DServerAPP_score` DISABLE KEYS */;
INSERT INTO `DServerAPP_score` VALUES (1,843,'2018-10-10 07:25:02.475003','207592',22),(2,620,'2018-10-10 07:25:02.586144','207592',21),(3,250,'2018-10-10 07:25:02.672842','207592',72),(4,230,'2018-10-10 07:25:02.749883','207592',23),(5,-267,'2018-10-10 07:25:02.835252','207592',36),(6,-347,'2018-10-10 07:25:02.927701','207592',37),(7,-417,'2018-10-10 07:25:03.029304','207592',38),(8,-443,'2018-10-10 07:25:03.111185','207592',39),(9,-469,'2018-10-10 07:25:03.197843','207592',40),(10,843,'2018-10-10 07:25:29.588740','207592',22),(11,620,'2018-10-10 07:25:29.674879','207592',21),(12,250,'2018-10-10 07:25:29.762103','207592',72),(13,230,'2018-10-10 07:25:29.843706','207592',23),(14,-267,'2018-10-10 07:25:29.932727','207592',36),(15,-347,'2018-10-10 07:25:30.019665','207592',37),(16,-417,'2018-10-10 07:25:30.105238','207592',38),(17,-443,'2018-10-10 07:25:30.192009','207592',39),(18,-469,'2018-10-10 07:25:30.276112','207592',40),(19,843,'2018-10-11 05:40:06.576627','207592',22),(20,620,'2018-10-11 05:40:06.675861','207592',21),(21,250,'2018-10-11 05:40:06.766555','207592',72),(22,230,'2018-10-11 05:40:06.850373','207592',23),(23,-267,'2018-10-11 05:40:06.941256','207592',36),(24,-347,'2018-10-11 05:40:07.039327','207592',37),(25,-417,'2018-10-11 05:40:07.124192','207592',38),(26,-443,'2018-10-11 05:40:07.218930','207592',39),(27,-469,'2018-10-11 05:40:07.310403','207592',40),(28,843,'2018-10-11 05:43:21.757649','207592',22),(29,620,'2018-10-11 05:43:21.850008','207592',21),(30,250,'2018-10-11 05:43:21.939029','207592',72),(31,230,'2018-10-11 05:43:22.021614','207592',23),(32,-267,'2018-10-11 05:43:22.107370','207592',36),(33,-347,'2018-10-11 05:43:22.197442','207592',37),(34,-417,'2018-10-11 05:43:22.283591','207592',38),(35,-443,'2018-10-11 05:43:22.367857','207592',39),(36,-469,'2018-10-11 05:43:22.454712','207592',40),(37,843,'2018-10-11 05:53:18.842222','207592',22),(38,620,'2018-10-11 05:53:18.939551','207592',21),(39,250,'2018-10-11 05:53:19.025451','207592',72),(40,230,'2018-10-11 05:53:19.111512','207592',23),(41,-267,'2018-10-11 05:53:19.199578','207592',36),(42,-347,'2018-10-11 05:53:19.281434','207592',37),(43,-417,'2018-10-11 05:53:19.369753','207592',38),(44,-443,'2018-10-11 05:53:19.459997','207592',39),(45,-469,'2018-10-11 05:53:19.550166','207592',40),(46,843,'2018-10-11 05:55:51.638743','207592',22),(47,620,'2018-10-11 05:55:51.728298','207592',21),(48,250,'2018-10-11 05:55:51.819668','207592',72),(49,230,'2018-10-11 05:55:51.901527','207592',23),(50,-267,'2018-10-11 05:55:51.988335','207592',36),(51,-347,'2018-10-11 05:55:52.081687','207592',37),(52,-417,'2018-10-11 05:55:52.167335','207592',38),(53,-443,'2018-10-11 05:55:52.256673','207592',39),(54,-469,'2018-10-11 05:55:52.340107','207592',40),(55,1741,'2018-10-12 07:16:26.114235','100524',21),(56,733,'2018-10-12 07:16:26.217962','100524',41),(57,719,'2018-10-12 07:16:26.309707','100524',53),(58,472,'2018-10-12 07:16:26.392131','100524',50),(59,35,'2018-10-12 07:16:26.475635','100524',54),(60,-166,'2018-10-12 07:16:26.564778','100524',32),(61,-763,'2018-10-12 07:16:26.647543','100524',33),(62,-892,'2018-10-12 07:16:26.729013','100524',48),(63,-1879,'2018-10-12 07:16:26.813077','100524',35),(64,6569,'2018-10-13 05:59:52.062500','205529',61),(65,121,'2018-10-13 05:59:52.151040','205529',62),(66,18,'2018-10-13 05:59:52.225637','205529',63),(67,-296,'2018-10-13 05:59:52.300041','205529',64),(68,-690,'2018-10-13 05:59:52.400853','205529',65),(69,-915,'2018-10-13 05:59:52.479935','205529',66),(70,-1236,'2018-10-13 05:59:52.551779','205529',67),(71,-1285,'2018-10-13 05:59:52.626457','205529',68),(72,-2286,'2018-10-13 05:59:52.701763','205529',69),(73,843,'2018-10-15 03:20:11.950115','207592',22),(74,620,'2018-10-15 03:20:11.998846','207592',21),(75,250,'2018-10-15 03:20:12.028527','207592',72),(76,230,'2018-10-15 03:20:12.058207','207592',23),(77,-267,'2018-10-15 03:20:12.084189','207592',36),(78,-347,'2018-10-15 03:20:12.135365','207592',37),(79,-417,'2018-10-15 03:20:12.164905','207592',38),(80,-443,'2018-10-15 03:20:12.189840','207592',39),(81,-469,'2018-10-15 03:20:12.216234','207592',40),(82,1771,'2018-10-15 03:46:46.453075','101439',42),(83,1173,'2018-10-15 03:46:46.563247','101439',21),(84,678,'2018-10-15 03:46:46.645036','101439',55),(85,268,'2018-10-15 03:46:46.725858','101439',49),(86,80,'2018-10-15 03:46:46.806539','101439',56),(87,-150,'2018-10-15 03:46:46.887744','101439',57),(88,-935,'2018-10-15 03:46:47.210371','101439',50),(89,-2311,'2018-10-15 03:46:47.298776','101439',59),(90,5300,'2018-10-15 03:48:23.783258','301395',21),(91,769,'2018-10-15 03:48:23.860513','301395',45),(92,516,'2018-10-15 03:48:23.937944','301395',48),(93,509,'2018-10-15 03:48:24.016067','301395',49),(94,-400,'2018-10-15 03:48:24.098347','301395',50),(95,-1231,'2018-10-15 03:48:24.176514','301395',33),(96,-1650,'2018-10-15 03:48:24.255211','301395',51),(97,-1878,'2018-10-15 03:48:24.344444','301395',52),(98,-1935,'2018-10-15 03:48:24.423000','301395',53),(99,5300,'2018-10-15 03:50:44.225185','301395',21),(100,769,'2018-10-15 03:50:44.333208','301395',45),(101,516,'2018-10-15 03:50:44.415914','301395',48),(102,509,'2018-10-15 03:50:44.501114','301395',49),(103,-400,'2018-10-15 03:50:44.584753','301395',50),(104,-1231,'2018-10-15 03:50:44.665211','301395',33),(105,-1650,'2018-10-15 03:50:44.749278','301395',51),(106,-1878,'2018-10-15 03:50:44.911478','301395',52),(107,-1935,'2018-10-15 03:50:45.027934','301395',53),(108,5300,'2018-10-15 03:53:07.281166','301395',21),(109,769,'2018-10-15 03:53:07.372497','301395',45),(110,516,'2018-10-15 03:53:07.463381','301395',48),(111,509,'2018-10-15 03:53:07.550630','301395',49),(112,-400,'2018-10-15 03:53:07.635306','301395',50),(113,-1231,'2018-10-15 03:53:07.721980','301395',33),(114,-1650,'2018-10-15 03:53:07.807459','301395',51),(115,-1878,'2018-10-15 03:53:07.894992','301395',52),(116,-1935,'2018-10-15 03:53:07.985606','301395',53),(117,5300,'2018-10-15 03:53:27.921454','301395',21),(118,769,'2018-10-15 03:53:28.016693','301395',45),(119,516,'2018-10-15 03:53:28.108495','301395',48),(120,509,'2018-10-15 03:53:28.204701','301395',49),(121,-400,'2018-10-15 03:53:28.289684','301395',50),(122,-1231,'2018-10-15 03:53:28.376480','301395',33),(123,-1650,'2018-10-15 03:53:28.466403','301395',51),(124,-1878,'2018-10-15 03:53:28.547281','301395',52),(125,-1935,'2018-10-15 03:53:28.692916','301395',53);
/*!40000 ALTER TABLE `DServerAPP_score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add choice',1,'add_choice'),(2,'Can change choice',1,'change_choice'),(3,'Can delete choice',1,'delete_choice'),(4,'Can view choice',1,'view_choice'),(5,'Can add question',2,'add_question'),(6,'Can change question',2,'change_question'),(7,'Can delete question',2,'delete_question'),(8,'Can view question',2,'view_question'),(9,'Can add clubs',3,'add_clubs'),(10,'Can change clubs',3,'change_clubs'),(11,'Can delete clubs',3,'delete_clubs'),(12,'Can view clubs',3,'view_clubs'),(13,'Can add game id',4,'add_gameid'),(14,'Can change game id',4,'change_gameid'),(15,'Can delete game id',4,'delete_gameid'),(16,'Can view game id',4,'view_gameid'),(17,'Can add player',5,'add_player'),(18,'Can change player',5,'change_player'),(19,'Can delete player',5,'delete_player'),(20,'Can view player',5,'view_player'),(21,'Can add score',6,'add_score'),(22,'Can change score',6,'change_score'),(23,'Can delete score',6,'delete_score'),(24,'Can view score',6,'view_score'),(25,'Can add history game',7,'add_historygame'),(26,'Can change history game',7,'change_historygame'),(27,'Can delete history game',7,'delete_historygame'),(28,'Can view history game',7,'view_historygame'),(29,'Can add log entry',8,'add_logentry'),(30,'Can change log entry',8,'change_logentry'),(31,'Can delete log entry',8,'delete_logentry'),(32,'Can view log entry',8,'view_logentry'),(33,'Can add permission',9,'add_permission'),(34,'Can change permission',9,'change_permission'),(35,'Can delete permission',9,'delete_permission'),(36,'Can view permission',9,'view_permission'),(37,'Can add group',10,'add_group'),(38,'Can change group',10,'change_group'),(39,'Can delete group',10,'delete_group'),(40,'Can view group',10,'view_group'),(41,'Can add user',11,'add_user'),(42,'Can change user',11,'change_user'),(43,'Can delete user',11,'delete_user'),(44,'Can view user',11,'view_user'),(45,'Can add content type',12,'add_contenttype'),(46,'Can change content type',12,'change_contenttype'),(47,'Can delete content type',12,'delete_contenttype'),(48,'Can view content type',12,'view_contenttype'),(49,'Can add session',13,'add_session'),(50,'Can change session',13,'change_session'),(51,'Can delete session',13,'delete_session'),(52,'Can view session',13,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'admin','logentry'),(10,'auth','group'),(9,'auth','permission'),(11,'auth','user'),(12,'contenttypes','contenttype'),(1,'DServerAPP','choice'),(3,'DServerAPP','clubs'),(4,'DServerAPP','gameid'),(7,'DServerAPP','historygame'),(5,'DServerAPP','player'),(2,'DServerAPP','question'),(6,'DServerAPP','score'),(13,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'DServerAPP','0001_initial','2018-10-09 02:26:26.531859'),(2,'DServerAPP','0002_auto_20180908_0911','2018-10-09 02:26:26.695411'),(3,'DServerAPP','0003_auto_20180911_1138','2018-10-09 02:26:26.719245'),(4,'DServerAPP','0004_auto_20180922_1123','2018-10-09 02:26:26.810728'),(5,'DServerAPP','0005_player_introducer','2018-10-09 02:26:26.842651'),(6,'DServerAPP','0006_auto_20180923_1503','2018-10-09 02:26:26.869800'),(7,'DServerAPP','0007_historygame','2018-10-09 02:26:26.909002'),(8,'DServerAPP','0008_auto_20180924_1217','2018-10-09 02:26:26.956093'),(9,'DServerAPP','0009_auto_20180924_1441','2018-10-09 02:26:26.985553'),(10,'DServerAPP','0010_auto_20180924_1441','2018-10-09 02:26:27.015418'),(11,'DServerAPP','0011_auto_20181002_1809','2018-10-09 02:26:27.084740'),(12,'DServerAPP','0012_auto_20181009_0225','2018-10-09 02:26:27.279695'),(13,'contenttypes','0001_initial','2018-10-09 02:26:27.339426'),(14,'auth','0001_initial','2018-10-09 02:26:27.740404'),(15,'admin','0001_initial','2018-10-09 02:26:27.806562'),(16,'admin','0002_logentry_remove_auto_add','2018-10-09 02:26:27.817568'),(17,'admin','0003_logentry_add_action_flag_choices','2018-10-09 02:26:27.829115'),(18,'contenttypes','0002_remove_content_type_name','2018-10-09 02:26:27.895004'),(19,'auth','0002_alter_permission_name_max_length','2018-10-09 02:26:27.921525'),(20,'auth','0003_alter_user_email_max_length','2018-10-09 02:26:27.952499'),(21,'auth','0004_alter_user_username_opts','2018-10-09 02:26:27.966159'),(22,'auth','0005_alter_user_last_login_null','2018-10-09 02:26:27.996851'),(23,'auth','0006_require_contenttypes_0002','2018-10-09 02:26:28.000550'),(24,'auth','0007_alter_validators_add_error_messages','2018-10-09 02:26:28.010580'),(25,'auth','0008_alter_user_username_max_length','2018-10-09 02:26:28.039755'),(26,'auth','0009_alter_user_last_name_max_length','2018-10-09 02:26:28.070266'),(27,'sessions','0001_initial','2018-10-09 02:26:28.119945');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('40i91855a8t4zofdi7io6slr7bs8ib2a','M2ViZTliMTRhOWYyZjhhNDFhOTFmY2VhYWQ0MTI3YjIxN2I2NGVkMzp7ImxvZ2luIjp0cnVlfQ==','2018-10-25 07:41:23.713194'),('bo23r1yjtk2pvqmiqs6a992nsxjby5eg','MjExMDljNTEwMjFmMWYwZWJjZjU5YTdjNjZmMjY0YWU1NGRkMmI4ZDp7ImxvZ2luIjp0cnVlLCJjbHViIjoiMTg4MTEzMzM5NjQifQ==','2018-10-29 03:17:13.425786'),('zcademcqr73waghkw681ng260palv2vr','NzYyMTBjMDg1MTlhOWI5MGUwYWVhNTQzM2VmZWQxOTI2MmNmNjIwODp7ImxvZ2luIjp0cnVlLCJjbHViIjoicXVkYW8ifQ==','2018-10-29 03:38:35.806438');
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

-- Dump completed on 2018-10-15 11:58:57

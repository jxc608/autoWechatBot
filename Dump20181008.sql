-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: auto_accounting
-- ------------------------------------------------------
-- Server version	5.7.15-log

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
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add choice',1,'add_choice'),(2,'Can change choice',1,'change_choice'),(3,'Can delete choice',1,'delete_choice'),(4,'Can view choice',1,'view_choice'),(5,'Can add question',2,'add_question'),(6,'Can change question',2,'change_question'),(7,'Can delete question',2,'delete_question'),(8,'Can view question',2,'view_question'),(9,'Can add log entry',3,'add_logentry'),(10,'Can change log entry',3,'change_logentry'),(11,'Can delete log entry',3,'delete_logentry'),(12,'Can view log entry',3,'view_logentry'),(13,'Can add permission',4,'add_permission'),(14,'Can change permission',4,'change_permission'),(15,'Can delete permission',4,'delete_permission'),(16,'Can view permission',4,'view_permission'),(17,'Can add group',5,'add_group'),(18,'Can change group',5,'change_group'),(19,'Can delete group',5,'delete_group'),(20,'Can view group',5,'view_group'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add content type',7,'add_contenttype'),(26,'Can change content type',7,'change_contenttype'),(27,'Can delete content type',7,'delete_contenttype'),(28,'Can view content type',7,'view_contenttype'),(29,'Can add session',8,'add_session'),(30,'Can change session',8,'change_session'),(31,'Can delete session',8,'delete_session'),(32,'Can view session',8,'view_session'),(33,'Can add player',9,'add_player'),(34,'Can change player',9,'change_player'),(35,'Can delete player',9,'delete_player'),(36,'Can view player',9,'view_player'),(37,'Can add score',10,'add_score'),(38,'Can change score',10,'change_score'),(39,'Can delete score',10,'delete_score'),(40,'Can view score',10,'view_score'),(41,'Can add game id',11,'add_gameid'),(42,'Can change game id',11,'change_gameid'),(43,'Can delete game id',11,'delete_gameid'),(44,'Can view game id',11,'view_gameid'),(45,'Can add clubs',12,'add_clubs'),(46,'Can change clubs',12,'change_clubs'),(47,'Can delete clubs',12,'delete_clubs'),(48,'Can view clubs',12,'view_clubs'),(49,'Can add history game',13,'add_historygame'),(50,'Can change history game',13,'change_historygame'),(51,'Can delete history game',13,'delete_historygame'),(52,'Can view history game',13,'view_historygame');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (3,'admin','logentry'),(5,'auth','group'),(4,'auth','permission'),(6,'auth','user'),(7,'contenttypes','contenttype'),(1,'DServerAPP','choice'),(12,'DServerAPP','clubs'),(11,'DServerAPP','gameid'),(13,'DServerAPP','historygame'),(9,'DServerAPP','player'),(2,'DServerAPP','question'),(10,'DServerAPP','score'),(8,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'DServerAPP','0001_initial','2018-09-07 10:07:49.085251'),(2,'contenttypes','0001_initial','2018-09-07 10:07:49.647343'),(3,'auth','0001_initial','2018-09-07 10:07:56.873073'),(4,'admin','0001_initial','2018-09-07 10:07:58.542538'),(5,'admin','0002_logentry_remove_auto_add','2018-09-07 10:07:58.591644'),(6,'admin','0003_logentry_add_action_flag_choices','2018-09-07 10:07:58.626620'),(7,'contenttypes','0002_remove_content_type_name','2018-09-07 10:07:59.600377'),(8,'auth','0002_alter_permission_name_max_length','2018-09-07 10:08:00.668052'),(9,'auth','0003_alter_user_email_max_length','2018-09-07 10:08:01.358841'),(10,'auth','0004_alter_user_username_opts','2018-09-07 10:08:01.393817'),(11,'auth','0005_alter_user_last_login_null','2018-09-07 10:08:02.062858'),(12,'auth','0006_require_contenttypes_0002','2018-09-07 10:08:02.168825'),(13,'auth','0007_alter_validators_add_error_messages','2018-09-07 10:08:02.216810'),(14,'auth','0008_alter_user_username_max_length','2018-09-07 10:08:02.930016'),(15,'auth','0009_alter_user_last_name_max_length','2018-09-07 10:08:03.545818'),(16,'sessions','0001_initial','2018-09-07 10:08:04.369744'),(17,'DServerAPP','0002_auto_20180908_0911','2018-09-08 01:11:35.218865'),(18,'DServerAPP','0003_auto_20180911_1138','2018-09-11 03:46:54.430324'),(19,'DServerAPP','0004_auto_20180922_1123','2018-09-22 03:23:49.980877'),(20,'DServerAPP','0005_player_introducer','2018-09-23 03:24:55.424594'),(21,'DServerAPP','0006_auto_20180923_1503','2018-09-23 07:09:24.252439'),(22,'DServerAPP','0007_historygame','2018-09-24 03:05:25.156757'),(23,'DServerAPP','0008_auto_20180924_1217','2018-09-24 04:18:00.441250'),(24,'DServerAPP','0009_auto_20180924_1441','2018-09-24 06:41:36.237447'),(25,'DServerAPP','0010_auto_20180924_1441','2018-09-24 06:41:36.988252'),(26,'DServerAPP','0011_auto_20181002_1809','2018-10-02 10:09:31.205795'),(27,'DServerAPP','0012_auto_20181008_2344','2018-10-08 15:45:09.375937');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `DServerAPP_choice`
--

LOCK TABLES `DServerAPP_choice` WRITE;
/*!40000 ALTER TABLE `DServerAPP_choice` DISABLE KEYS */;
/*!40000 ALTER TABLE `DServerAPP_choice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `DServerAPP_clubs`
--

LOCK TABLES `DServerAPP_clubs` WRITE;
/*!40000 ALTER TABLE `DServerAPP_clubs` DISABLE KEYS */;
INSERT INTO `DServerAPP_clubs` VALUES ('7cf6be1cbf0111e881a63497f629cee7','18811333964','34weah324n',1540279525.197402,0,'none',0),('abbd86f4beff11e8b1773497f629cee7','balana608','18811333964',1537686594.206284,0,'none',0);
/*!40000 ALTER TABLE `DServerAPP_clubs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `DServerAPP_gameid`
--

LOCK TABLES `DServerAPP_gameid` WRITE;
/*!40000 ALTER TABLE `DServerAPP_gameid` DISABLE KEYS */;
INSERT INTO `DServerAPP_gameid` VALUES (1,'梓','251566',2),(2,'七子','299358',29),(4,'斌斌xxx','179754',30),(5,'贷款','496687',31),(6,'因果','387464',32),(7,'wbh','10784',33),(8,'一碗饭、','429580',34),(9,'Mr.翁','326710',35),(10,'b\'\\xf0\\x9f\\x8c\\xb9\'','637665',21),(11,'b\'\\xe4\\xb8\\xa5\\xe5\\xbb\\xb6\\xe8\\xb4\\xb5\'','550839',22),(12,'b\'\\xe5\\x8a\\x9d\\xe5\\x90\\x9b\'','557419',72),(13,'b\'\\xe6\\x94\\xbe\\xe7\\xba\\xb5\'','451835',23),(14,'b\'\\xe5\\x8f\\xb6\\xe5\\xad\\x90\'','540000',36),(15,'b\'\\xe3\\x80\\x82\'','350478',37),(16,'b\'\\xe5\\xbf\\x83\\xe5\\x93\\xa5\'','387616',38),(17,'b\'\\xe6\\x83\\x85\\xe8\\xb0\\x8a\'','415598',39),(18,'b\'\\xe9\\x99\\x88\\xe7\\x81\\xbf\\xe4\\xbb\\x81\'','370886',40),(19,'b\'\\xe9\\xbe\\x99\\xe8\\xa1\\x8c\\xe5\\xa4\\xa9\\xe4\\xb8\\x8b\'','357712',41),(20,'b\'\\xe5\\xa4\\x95\\xe9\\x98\\xb3\'','596618',42),(21,'b\'\\xef\\xbc\\x81\\xef\\xbc\\x81\'','170281',43),(22,'b\'^_^\\xe7\\xa6\\x8f\'','637115',44),(23,'b\'\\xe5\\xa3\\xb9=\\xe5\\xa3\\xb9\'','249591',45),(24,'b\'\\xe9\\x8e\\x8f\\xe7\\x85\\x8c\'','624713',46),(25,'b\'rose\'','22583',47),(26,'b\'\\xe4\\xbd\\xa0\\xe7\\x9a\\x84\\xe5\\x90\\x8d\\xe5\\xad\\x97\'','421027',48),(27,'b\'\\xe6\\x96\\x8c\\xe6\\x96\\x8c\'','218525',49),(28,'b\'.\'','243636',50),(29,'b\'casual\'','170219',51),(30,'b\'\\xe8\\xbf\\x87\\xe5\\xbe\\x80\'','390822',52),(31,'b\'\\xe7\\xae\\x80\\xe5\\x8d\\x95\'','299079',53),(32,'b\'\\xe5\\x8f\\x9b\\xe9\\x80\\x86\'','372566',54),(33,'b\'miki\'','640560',55),(34,'b\'ioco\\xe3\\x80\\x82\'','358411',56),(35,'b\'\\xe6\\x88\\x90\\xe6\\xb5\\xa91\'','348330',57),(36,'b\'bin\'','367460',58),(37,'b\'\\xe9\\x98\\xbf\\xe5\\xbc\\xba\'','636449',59),(38,'b\'\\xe4\\xba\\xb2\\xe4\\xba\\xb2\\xe4\\xba\\xb2\'','317900',60),(39,'b\'\\xe9\\x9d\\x92\\xe5\\xb1\\xb1\'','468312',61),(40,'b\'\\xe4\\xb8\\x8b\\xe5\\xad\\x90\\xe7\\xa7\\x92\'','498096',62),(41,'b\'\\xe9\\xa3\\x9e\\xe9\\xbe\\x99\\xe5\\x8f\\xb7\'','108135',63),(42,'b\'\\xe7\\xa6\\xb9\\xe8\\xb1\\xaa\'','132870',64),(43,'b\'aa\\xe5\\xb0\\x8f\'','491532',65),(44,'b\'\\xe5\\x9b\\xbd\\xe9\\x99\\x85\\xe7\\xad\\xbe\\xe8\\xaf\\x81\'','570529',66),(45,'b\'\\xe5\\xa4\\xa9\\xe5\\xa4\\xa9\\xe5\\xbc\\x80\\xe5\\xbf\\x83\'','606368',67),(46,'b\'\\xe5\\xb0\\x8f\\xe6\\x9e\\x97\'','491026',68),(47,'b\'\\xe9\\x99\\x8c\\xe8\\xb7\\xaf\'','636591',69),(48,'b\'\\xe4\\xbd\\x99\\xe7\\x94\\x9f\'','196586',70),(49,'b\'\\xe4\\xb8\\x89\\xe8\\x97\\x8f\'','328743',71);
/*!40000 ALTER TABLE `DServerAPP_gameid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `DServerAPP_historygame`
--

LOCK TABLES `DServerAPP_historygame` WRITE;
/*!40000 ALTER TABLE `DServerAPP_historygame` DISABLE KEYS */;
/*!40000 ALTER TABLE `DServerAPP_historygame` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `DServerAPP_player`
--

LOCK TABLES `DServerAPP_player` WRITE;
/*!40000 ALTER TABLE `DServerAPP_player` DISABLE KEYS */;
INSERT INTO `DServerAPP_player` VALUES (1,'','流觞','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(2,'','旭宝','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(4,'','星钰','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(5,'','赌神','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(6,'','助手','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(7,'','小刀','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(8,'','高进','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(9,'','知足','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(10,'','放手','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(11,'','实例','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(12,'','粑粑','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(13,'','便便','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(14,'','七子','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(15,'','斌斌xxx','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(16,'','AA贷款专科','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(17,'','因果','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(18,'','wbh','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(19,'','一碗饭、','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(20,'','Mr.翁','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(21,'','b\'\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(22,'','b\'\\xe4\\xb8\\xa5\\xe5\\xbb\\xb6\\xe8\\xb4\\xb5\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(23,'','b\'\\xe6\\x94\\xbe\\xe7\\xba\\xb5\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(24,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(25,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(26,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(27,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(28,'','b\'\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\\xf0\\x9f\\x8c\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(29,'','b\'\\xe4\\xb8\\x83\\xe5\\xad\\x90\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(30,'','b\'\\xe6\\x96\\x8c\\xe6\\x96\\x8cxxx\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(31,'','b\'AA\\xe8\\xb4\\xb7\\xe6\\xac\\xbe\\xe4\\xb8\\x93\\xe7\\xa7\\x91\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(32,'','b\'\\xe5\\x9b\\xa0\\xe6\\x9e\\x9c\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(33,'','b\'wbh\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(34,'','b\'\\xe4\\xb8\\x80\\xe7\\xa2\\x97\\xe9\\xa5\\xad\\xe3\\x80\\x81\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(35,'','b\'Mr.\\xe7\\xbf\\x81\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(36,'','b\'\\xe5\\x8f\\xb6\\xe5\\xad\\x90\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(37,'','b\'\\xe3\\x80\\x82\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(38,'','b\'\\xe5\\xbf\\x83\\xe5\\x93\\xa5\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(39,'','b\'\\xe6\\x83\\x85\\xe8\\xb0\\x8a\\xe3\\x80\\x81\\xe5\\xa4\\xa9\\xe4\\xb8\\x8b\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(40,'','b\'\\xe9\\x99\\x88\\xe7\\x81\\xbf\\xe4\\xbb\\x81\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(41,'','b\'\\xe9\\xbe\\x99\\xe8\\xa1\\x8c\\xe5\\xa4\\xa9\\xe4\\xb8\\x8b\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(42,'','b\'\\xe5\\xa4\\x95\\xe9\\x98\\xb3\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(43,'','b\'\\xef\\xbc\\x81\\xef\\xbc\\x81\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(44,'','b\'\\xf0\\x9f\\x98\\x8a\\xe7\\xa6\\x8f\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(45,'','b\'\\xe5\\xa3\\xb9=\\xe5\\xa3\\xb9\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(46,'','b\'\\xe9\\x8e\\x8f\\xe7\\x85\\x8c\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(47,'','b\'rose\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(48,'','b\'\\xe4\\xbd\\xa0\\xe7\\x9a\\x84\\xe5\\x90\\x8d\\xe5\\xad\\x97\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(49,'','b\'\\xe6\\x96\\x8c\\xe6\\x96\\x8c\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(50,'','b\'.\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(51,'','b\'casual\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(52,'','b\'\\xe8\\xbf\\x87\\xe5\\xbe\\x80\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(53,'','b\'\\xe7\\xae\\x80\\xe5\\x8d\\x95\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(54,'','b\'\\xe5\\x8f\\x9b\\xe9\\x80\\x86\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(55,'','b\'miki\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(56,'','b\'ioco\\xe3\\x80\\x82\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(57,'','b\'\\xe6\\x88\\x90\\xe6\\xb5\\xa91\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(58,'','b\'bin\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(59,'','b\'\\xe9\\x98\\xbf\\xe5\\xbc\\xba\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(60,'','b\'\\xe4\\xba\\xb2\\xe4\\xba\\xb2\\xe4\\xba\\xb2\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(61,'','b\'\\xe9\\x9d\\x92\\xe5\\xb1\\xb1\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(62,'','b\'\\xe4\\xb8\\x8b\\xe5\\xad\\x90\\xe7\\xa7\\x92\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(63,'','b\'\\xe9\\xa3\\x9e\\xe9\\xbe\\x99\\xe5\\x8f\\xb7\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(64,'','b\'\\xe7\\xa6\\xb9\\xe8\\xb1\\xaa\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(65,'','b\'aa\\xe5\\xb0\\x8f\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(66,'','b\'\\xe5\\x9b\\xbd\\xe9\\x99\\x85\\xe7\\xad\\xbe\\xe8\\xaf\\x81\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(67,'','b\'\\xe5\\xa4\\xa9\\xe5\\xa4\\xa9\\xe5\\xbc\\x80\\xe5\\xbf\\x83\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(68,'','b\'\\xe5\\xb0\\x8f\\xe6\\x9e\\x97\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(69,'','b\'\\xe9\\x99\\x8c\\xe8\\xb7\\xaf\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(70,'','b\'\\xe4\\xbd\\x99\\xe7\\x94\\x9f\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(71,'','b\'\\xe4\\xb8\\x89\\xe8\\x97\\x8f\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0),(72,'','b\'\\xe5\\x8a\\x9d\\xe5\\x90\\x9b\\xe8\\x8e\\xab\\xe6\\x89\\xa7\\xe6\\x84\\x8f\'','7cf6be1cbf0111e881a63497f629cee7',0,0,'none',0);
/*!40000 ALTER TABLE `DServerAPP_player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `DServerAPP_question`
--

LOCK TABLES `DServerAPP_question` WRITE;
/*!40000 ALTER TABLE `DServerAPP_question` DISABLE KEYS */;
/*!40000 ALTER TABLE `DServerAPP_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `DServerAPP_score`
--

LOCK TABLES `DServerAPP_score` WRITE;
/*!40000 ALTER TABLE `DServerAPP_score` DISABLE KEYS */;
/*!40000 ALTER TABLE `DServerAPP_score` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-08 23:48:52

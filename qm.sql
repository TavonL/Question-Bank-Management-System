-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: qm
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `figure`
--

DROP TABLE IF EXISTS `figure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `figure` (
  `figure_url` varchar(45) NOT NULL,
  `question_no` int(11) unsigned NOT NULL,
  `A/Q` varchar(3) NOT NULL,
  PRIMARY KEY (`figure_url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='图片(图片url，大题题号，A/Q)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `figure`
--

LOCK TABLES `figure` WRITE;
/*!40000 ALTER TABLE `figure` DISABLE KEYS */;
INSERT INTO `figure` VALUES ('..\\db_figure\\1.jpg',3,'Q');
/*!40000 ALTER TABLE `figure` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gs_cor`
--

DROP TABLE IF EXISTS `gs_cor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `gs_cor` (
  `grade` int(11) NOT NULL,
  `subject` int(11) unsigned NOT NULL,
  PRIMARY KEY (`grade`,`subject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='年级科目对应表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gs_cor`
--

LOCK TABLES `gs_cor` WRITE;
/*!40000 ALTER TABLE `gs_cor` DISABLE KEYS */;
INSERT INTO `gs_cor` VALUES (1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3),(4,1),(4,2),(4,3),(5,1),(5,2),(5,3),(6,1),(6,2),(6,3),(7,1),(7,2),(7,3),(8,1),(8,2),(8,3),(8,4),(9,1),(9,2),(9,3),(9,4),(9,5),(9,9),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(11,1),(11,2),(11,3),(11,4),(11,5),(11,6),(11,7),(11,8),(11,9),(12,1),(12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(12,8),(12,9);
/*!40000 ALTER TABLE `gs_cor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `know`
--

DROP TABLE IF EXISTS `know`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `know` (
  `know_no` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `know_name` varchar(45) NOT NULL,
  `super_no` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`know_no`),
  UNIQUE KEY `know_name_UNIQUE` (`know_name`),
  KEY `A_idx` (`super_no`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `know`
--

LOCK TABLES `know` WRITE;
/*!40000 ALTER TABLE `know` DISABLE KEYS */;
INSERT INTO `know` VALUES (1,'语文',NULL),(2,'数学',NULL),(3,'英语',NULL),(4,'物理',NULL),(5,'化学',NULL),(6,'生物',NULL),(7,'地理',NULL),(8,'历史',NULL),(9,'政治',NULL),(10,'几何',2),(11,'立体几何',10),(12,'解析几何',10),(13,'椭圆',12),(14,'双曲线',12),(15,'抛物线',12),(16,'代数',2),(17,'三角函数',16),(18,'热学',4),(19,'电磁学',4),(20,'近代物理',4),(21,'力学',4),(22,'光学',4),(23,'气体',18),(24,'分子热运动',18),(25,'内能',18),(27,'交流电',19),(28,'电磁感应',19),(29,'磁场',19),(30,'恒定电流',19),(31,'电场',19),(32,'原子核',20),(33,'原子',20),(34,'波',21),(35,'动量',21),(36,'运动',21),(37,'牛顿运动定律',21),(38,'功和能',21),(39,'光的传播',22),(40,'光的性质',22);
/*!40000 ALTER TABLE `know` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kq_cor`
--

DROP TABLE IF EXISTS `kq_cor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `kq_cor` (
  `question_no` int(11) unsigned NOT NULL,
  `know_no` int(11) unsigned NOT NULL,
  PRIMARY KEY (`question_no`,`know_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='题目知识点对应表（题号，知识点号）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kq_cor`
--

LOCK TABLES `kq_cor` WRITE;
/*!40000 ALTER TABLE `kq_cor` DISABLE KEYS */;
INSERT INTO `kq_cor` VALUES (1,16),(2,33),(3,39),(4,40),(5,32);
/*!40000 ALTER TABLE `kq_cor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `little_question`
--

DROP TABLE IF EXISTS `little_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `little_question` (
  `little_question_no` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `little_question_type` varchar(20) NOT NULL,
  `little_question_content` mediumtext,
  `little_question_answer` mediumtext,
  `little_question_analy` mediumtext,
  `super_question_no` int(11) unsigned NOT NULL,
  PRIMARY KEY (`little_question_no`),
  KEY `H_idx` (`super_question_no`),
  CONSTRAINT `H` FOREIGN KEY (`super_question_no`) REFERENCES `question` (`question_no`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COMMENT='小题目（题号，题型，题目文本，答案文本，题目解析）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `little_question`
--

LOCK TABLES `little_question` WRITE;
/*!40000 ALTER TABLE `little_question` DISABLE KEYS */;
INSERT INTO `little_question` VALUES (1,'应用题','地面对斜面的摩擦力大小与方向',NULL,NULL,6),(2,'应用题','地面对斜面的支持力大小',NULL,NULL,6),(3,'应用题','通过计算证明木块在此过程中满足动能定理',NULL,NULL,6);
/*!40000 ALTER TABLE `little_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paper`
--

DROP TABLE IF EXISTS `paper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `paper` (
  `paper_no` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `paper_subject` int(11) unsigned NOT NULL,
  `grade` int(11) NOT NULL,
  `paper_info` varchar(200) NOT NULL,
  `source` int(11) unsigned NOT NULL,
  PRIMARY KEY (`paper_no`),
  KEY `L` (`source`),
  KEY `B_idx` (`paper_subject`),
  CONSTRAINT `B` FOREIGN KEY (`paper_subject`) REFERENCES `know` (`know_no`),
  CONSTRAINT `L` FOREIGN KEY (`source`) REFERENCES `school` (`school_no`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COMMENT='试卷（试卷编号，科目，年级，试卷信息，学校名）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paper`
--

LOCK TABLES `paper` WRITE;
/*!40000 ALTER TABLE `paper` DISABLE KEYS */;
INSERT INTO `paper` VALUES (1,2,10,'2018-2019第一学期期中试卷',18),(2,4,12,'2009-2010年普通高等学校招生统一考试',1),(3,4,12,'2009-2010年高等学校招生统一考试',1),(4,4,12,'12',1),(10,9,12,'9210年测试卷',2),(11,9,12,'9210年测试卷',2),(12,9,12,'9210年测试卷',2),(13,9,12,'9210年测试卷',2);
/*!40000 ALTER TABLE `paper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `question` (
  `question_no` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `paper_no` int(11) unsigned NOT NULL,
  `question_type` varchar(20) NOT NULL,
  `question_diff` int(11) NOT NULL,
  `question_content` mediumtext,
  `question_answer` mediumtext,
  `question_analy` mediumtext,
  `know_no` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`question_no`),
  KEY `D_idx` (`paper_no`),
  KEY `I_idx` (`know_no`),
  CONSTRAINT `E` FOREIGN KEY (`paper_no`) REFERENCES `paper` (`paper_no`),
  CONSTRAINT `I` FOREIGN KEY (`know_no`) REFERENCES `know` (`know_no`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COMMENT='题目（题号，试卷号，题型，难度系数，题目文本，题目答案，题目解析，考察知识点）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,1,'填空题',1,'1+1=','2',NULL,16),(2,2,'单选题',1,'卢瑟福提出了原子的核式结构模型，这一模型建立的基础是(A) 粒子的散射实验(B)对阴极射线的研究(C)天然放射性现象的发现(D)质子的发现','A','卢瑟福根据α粒子的散射实验结果，提出了院子的核式结构模型：原子核聚集了院子的全部正电荷和几乎全部质量，电子在核外绕核运转。',33),(3,2,'单选题',1,'利用发波水槽得到的水面波形如a,b所示，则(A)图a、b均显示了波的干涉现象(B)图a、b均显示了波的衍射现象(C)图a显示了波的干涉现象，图b显示了波的衍射现象(D)图a显示了波的衍射现象，图b显示了波的干涉现象','D',NULL,39),(4,2,'单选题',1,'声波能绕过某一建筑物传播而光波却不能绕过该建筑物，这是因为(A)声波是纵波，光波是横波(B)声波振幅大，光波振幅小(C)声波波长较长，光波波长很短(D)声波波速较小，光波波速很大','C','本题考查波的衍射条件：障碍物与波长相差不多。',40),(5,2,'单选题',1,'现已建成的核电站的能量来自于(A)天然放射性元素衰变放出的能量(B)人工放射性同位素放出的的能量(C)重核裂变放出的能量(D)化学反应放出的能量','C',NULL,32),(6,2,'综合题',3,'倾角&theta;=37&deg;，质量M=5kg的粗糙斜面位于水平地面上，质量m=2kg的木块置于斜面顶端，从静止开始匀加速下滑，经t=2s到达底端，运动路程L=4m,在此过程中斜面保持静止,求：',NULL,NULL,37);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `school`
--

DROP TABLE IF EXISTS `school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `school` (
  `school_no` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `school_name` varchar(45) NOT NULL,
  `school_nature` varchar(45) NOT NULL,
  `super_no` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`school_no`),
  UNIQUE KEY `school_name_UNIQUE` (`school_name`) /*!80000 INVISIBLE */,
  KEY `K_idx` (`super_no`),
  CONSTRAINT `K` FOREIGN KEY (`super_no`) REFERENCES `school` (`school_no`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COMMENT='学校（学校名，学校性质）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `school`
--

LOCK TABLES `school` WRITE;
/*!40000 ALTER TABLE `school` DISABLE KEYS */;
INSERT INTO `school` VALUES (1,'上海市','国家级',NULL),(2,'浦东新区','市级',1),(3,'黄浦区','市级',1),(4,'静安区','市级',1),(5,'徐汇区','市级',1),(6,'长宁区','市级',1),(7,'普陀区','市级',1),(8,'虹口区','市级',1),(9,'杨浦区','市级',1),(10,'宝山区','市级',1),(11,'闵行区','市级',1),(12,'嘉定区','市级',1),(13,'金山区','市级',1),(14,'松江区','市级',1),(15,'青浦区','市级',1),(16,'奉贤区','市级',1),(17,'崇明区','市级',1),(18,'测试高中','公立',10);
/*!40000 ALTER TABLE `school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `user_name` varchar(45) NOT NULL,
  `user_pwd` varchar(45) NOT NULL,
  `user_auth` varchar(20) NOT NULL,
  PRIMARY KEY (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户（用户名，密码，权限）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('123','654321','试题录入员'),('丁二','123456','试题录入员'),('张三','123456','超级用户'),('王一','123456','试题管理员');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-05-26 22:51:54

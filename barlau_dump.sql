-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: barlau_db
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_phone_verified` tinyint(1) NOT NULL,
  `firebase_uid` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `current_latitude` decimal(9,6) DEFAULT NULL,
  `current_longitude` decimal(9,6) DEFAULT NULL,
  `last_location_update` datetime(6) DEFAULT NULL,
  `position` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `experience` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `education` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `skills` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `photo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `certifications` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `languages` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `about_me` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `achievements` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `age` int unsigned DEFAULT NULL,
  `courses` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `desired_salary` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hobbies` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `key_skills` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `linkedin` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `location` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `portfolio_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `publications` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `recommendations` longtext COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT (_utf8mb3''),
  `skype` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `recommendation_file` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `accounts_user_email_b2644a56_uniq` (`email`),
  UNIQUE KEY `firebase_uid` (`firebase_uid`),
  CONSTRAINT `accounts_user_chk_1` CHECK ((`age` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$870000$R4AZyfWUPDAFHbcs02Z7hm$UEiw/M4nr7fg1HPg0GSrtNLXyoXqhwBhGX0w1LHN1J4=','2025-05-30 20:18:07.077147',1,'admin','Маргулан','Беркинбаев',1,1,'2025-05-28 10:03:20.761763','admin@gmail.com','+77777777777','SUPERADMIN',0,NULL,NULL,NULL,NULL,'Разработчик','','','','employee_photos/364534896_313106267855822_2439338549827965295_n.jpg','','','','',NULL,'','','','','','','','','','','',0),(11,'pbkdf2_sha256$870000$HQRoajKtEEaBUuiuGgKn2P$3pNP8mdKHhxaLjzBge7k8j82cR8Xnf8wiZG6Iae7PRI=','2025-06-15 18:28:45.784059',0,'serik.aidarbe','Серик','Айдарбеков',0,1,'2025-05-30 10:53:45.282005','serik.aidarbek@barlau.org','+77757599686','DIRECTOR',0,NULL,NULL,NULL,NULL,'Директор','2010-2025: Директор ТОО \"Barlau\" - Управление всеми аспектами деятельности логистической компании\r\n2005-2010: Заместитель директора ООО \"КазЛогистик\" - Координация операционной деятельности','КазНУ им. аль-Фараби, экономический факультет (1995-2000). MBA в области логистики, Международный университет бизнеса (2005-2007).','','employee_photos/1.png','• Увеличение оборота компании в 3 раза\r\n• Открытие 5 новых филиалов\r\n• Команда года 2022-2024','Казахский (родной), Русский (свободно), Английский (продвинутый), Китайский (базовый)','Опытный руководитель с более чем 15-летним стажем в логистической отрасли. Специализируюсь на стратегическом планировании и развитии транспортных компаний.','• Увеличил прибыль компании на 150% за последние 5 лет\n• Расширил автопарк с 15 до 45 единиц техники\n• Внедрил систему GPS мониторинга для всего автопарка\n• Получил сертификат \"Лучший логистический директор года\" (2022)',45,'• Курс \"Современные технологии в логистике\" - Назарбаев Университет (2023)\n• \"Цифровая трансформация бизнеса\" - Business School Almaty (2022)\n• \"Лидерство в кризисных условиях\" - Harvard Business School Online (2021)','800000','Горный туризм, чтение книг по бизнесу, игра в теннис, фотография','Стратегическое планирование, управление персоналом, развитие бизнеса, логистика, финансовое планирование, ведение переговоров','','Алматы, Казахстан','','Статьи в журнале \"Логистика Казахстана\": \"Оптимизация транспортных маршрутов\" (2023), \"Цифровизация логистики\" (2022)','Рекомендательные письма от партнеров: ТОО \"Казахстан Темир Жолы\", ООО \"Евразия Логистик\", АО \"КазМунайГаз\"','','',0),(12,'pbkdf2_sha256$870000$rctBYX9sUkBMkNLw3S0z51$rp2LJJzZya6i5wO+kFRNMv67/C4azw+awPp7yGa3Xdc=',NULL,0,'almas.sopashev','Алмас','Сопашев',0,1,'2025-05-30 10:53:46.092470','almas.sopashev@barlau.org','+77771234568','DISPATCHER',0,NULL,NULL,NULL,NULL,'Заместитель директора и главный диспетчер грузовых перевозок','2015-2025: Заместитель директора и главный диспетчер ТОО \"Barlau\" - Координация перевозок, управление диспетчерской службой\r\n2010-2015: Старший диспетчер ООО \"АвтоТранс\" - Планирование маршрутов, контроль выполнения рейсов','Алматинский технологический университет, факультет транспорта и логистики (2000-2005). Повышение квалификации по управлению персоналом (2018).','','employee_photos/2.png','','Казахский (родной), Русский (свободно), Английский (средний)','Профессиональный диспетчер с глубоким пониманием транспортной логистики. Обеспечиваю эффективную координацию всех грузоперевозок компании.','• Сократил время простоя автотранспорта на 30%\n• Внедрил электронную систему диспетчеризации\n• Организовал обучение 25+ новых водителей\n• Получил звание \"Лучший диспетчер региона\" (2021)',38,'• \"Современные технологии диспетчеризации\" - АТУ (2023)\n• \"Управление логистическими процессами\" - КазАТУ (2022)\n• \"Охрана труда на транспорте\" - Центр Безопасности (2021)','600000','Автомобили, радиосвязь, рыбалка, шахматы','Диспетчеризация грузоперевозок, планирование маршрутов, управление персоналом, работа с GPS системами, документооборот','','Алматы, Казахстан','','','Рекомендации от водителей компании и партнеров по грузоперевозкам','','',0),(13,'pbkdf2_sha256$870000$QwO8xtsSBjkkH9KSXBptlS$FMVQ15u4hDih2EYPvHL0JzEHgMo5dFWrtYOCC11+ccY=',NULL,0,'erbolat.kudaibergen','Ерболат','Кудайбергенов',0,1,'2025-05-30 10:53:47.067264','erbolat.kudaibergen@barlau.org','+77771234569','MANAGER',0,NULL,NULL,NULL,NULL,'Начальник автобазы','2012-2025: Начальник автобазы ТОО \"Barlau\" - Управление автопарком, техническое обслуживание\r\n2007-2012: Главный механик ООО \"КазАвто\" - Ремонт и обслуживание грузовых автомобилей\r\n2002-2007: Слесарь-механик АО \"Автосервис+\" - Диагностика и ремонт двигателей','Алматинский политехнический колледж, специальность \"Техническое обслуживание автомобилей\" (1998-2002). Курсы повышения квалификации по современным автотехнологиям.','','employee_photos/3.png','','Казахский (родной), Русский (свободно), Английский (базовый)','Опытный руководитель автобазы с техническим образованием. Отвечаю за техническое состояние и эксплуатацию всего автопарка компании.','• Увеличил ресурс работы автопарка на 25%\n• Сократил расходы на ремонт на 20% за счет планового ТО\n• Внедрил систему учета запчастей и ГСМ\n• Организовал собственную ремонтную мастерскую',42,'• \"Современные системы диагностики автомобилей\" - Mercedes-Benz Training (2023)\n• \"Управление автопарком\" - Scania Academy (2022)\n• \"Экономия топлива и экологичность\" - Volvo Trucks (2021)','550000','Автомеханика, мотоциклы, футбол, самоделки','Управление автопарком, техническое обслуживание, диагностика, планирование ремонтов, управление персоналом','','Алматы, Казахстан','','','Положительные отзывы от водителей и технических специалистов','','',0),(14,'pbkdf2_sha256$870000$S15Dg5pVahHWxM0UFuIi9H$CZgHYcWblJtX6GTU/YM+8a/exLLDyb52e7qqUcHCMkI=',NULL,0,'nazerke.sadvakasova','Назерке','Садвакасова',0,1,'2025-05-30 10:53:47.832953','nazerke.sadvakasova@barlau.org','+77771234570','ACCOUNTANT',0,NULL,NULL,NULL,NULL,'Главный бухгалтер','2008-2025: Главный бухгалтер ТОО \"Barlau\" - Ведение полного учета, составление отчетности\r\n2003-2008: Бухгалтер ООО \"ТрансЛогистик\" - Учет ТМЦ, расчет зарплаты\r\n1998-2003: Помощник бухгалтера ТОО \"АлматыАвто\" - Первичная документация','Казахский экономический университет им. Т.Рыскулова, факультет учета и аудита (1993-1998). Курсы повышения квалификации по международным стандартам учета.','','employee_photos/4.png','Сертификат профессионального бухгалтера Казахстана, Удостоверение по налоговому учету\r\n• Автоматизировала учетные процессы на 90%','Казахский (родной), Русский (свободно), Английский (средний)','Квалифицированный главный бухгалтер с многолетним опытом в транспортной отрасли. Обеспечиваю точность финансовой отчетности и налогового планирования.','• Автоматизировала учетные процессы на 90%\n• Сократила время составления отчетности в 2 раза\n• Внедрила систему бюджетирования\n• Получила награду \"Лучший бухгалтер транспортной отрасли\" (2020)',35,'• \"Цифровая отчетность и ЭЦП\" - Палата Налоговых консультантов (2023)\n• \"МСФО для малого и среднего бизнеса\" - ACCA (2022)\n• \"1С:Предприятие 8.3 - продвинутый курс\" - 1С (2021)','450000','Чтение, вязание, садоводство, кулинария','Бухгалтерский учет, налоговое планирование, составление отчетности, работа с 1С, финансовый анализ','','Алматы, Казахстан','','','Рекомендации от налоговых консультантов и аудиторских компаний','','',0),(15,'pbkdf2_sha256$870000$e22EacTwUmH3xhYCPO19ef$xiwBiXeYzT8P9DxeW3xibX+bmzkKNvwFvLqV4Agfe3g=',NULL,0,'maksat.kusaiyn','Максат','Кусайын',0,1,'2025-05-30 10:53:48.608714','maksat.kusaiyn@barlau.org','+77771234571','IT_MANAGER',0,NULL,NULL,NULL,NULL,'Начальник службы логистики и IT программирования','2018-2025: Начальник службы логистики и IT ТОО \"Barlau\" - Внедрение IT-систем, оптимизация логистики\r\n2015-2018: Системный администратор ООО \"ТехЛогистик\" - Поддержка IT-инфраструктуры\r\n2012-2015: Программист ТОО \"SoftKZ\" - Разработка логистических систем','Казахский национальный технический университет им. К.Сатпаева, факультет информационных технологий (2007-2012). Магистратура по логистике в КазНУ (2016-2018).','','employee_photos/5.png','Сертификат Microsoft Certified: Azure Administrator, Cisco Certified Network Associate (CCNA)\r\n• Внедрил систему GPS-мониторинга для всего автопарка','Казахский (родной), Русский (свободно), Английский (продвинутый)','IT-менеджер и логист с техническим образованием. Отвечаю за цифровизацию логистических процессов и развитие IT-инфраструктуры компании.','• Внедрил систему GPS-мониторинга для всего автопарка\n• Разработал собственную систему диспетчеризации\n• Автоматизировал процесс планирования маршрутов\n• Сократил операционные расходы на 15% за счет оптимизации',32,'• \"Искусственный интеллект в логистике\" - MIT (2023)\n• \"Управление IT-проектами\" - PMI (2022)\n• \"Облачные технологии для бизнеса\" - Google Cloud (2021)','700000','Программирование, гаджеты, киберспорт, фотография дронами','Программирование, системное администрирование, логистическое планирование, управление проектами, внедрение IT-решений','','Алматы, Казахстан','https://github.com/maksat-barlau','','Рекомендации от IT-компаний и клиентов по внедренным решениям','','',0),(16,'pbkdf2_sha256$870000$riM0YB5CF8FX4BEZ1F5bfX$33i1UeL07AMiQUDqqLXAbsxkpCENvZdK/4XHMfssmSU=',NULL,0,'gabit.akhmetov','Габит','Ахметов',0,1,'2025-05-30 10:53:49.423785','gabit.akhmetov@barlau.org','+77771234572','SUPPLIER',0,NULL,NULL,NULL,NULL,'Снабженец','2010-2025: Снабженец ТОО \"Barlau\" - Закупка запчастей, ГСМ, расходных материалов\r\n2005-2010: Менеджер по закупкам ООО \"АвтоПарк\" - Работа с поставщиками','Алматинский экономический колледж, специальность \"Коммерция\" (1995-2000).','','employee_photos/6.png','','Казахский (родной), Русский (свободно), Турецкий (базовый)','Профессиональный снабженец с опытом работы в транспортной отрасли. Обеспечиваю своевременное снабжение компании всем необходимым.','• Снизил затраты на закупки на 18% за счет поиска новых поставщиков\n• Внедрил систему планирования закупок\n• Создал базу надежных поставщиков (50+ компаний)\n• Организовал эффективную систему складского учета',29,'• \"Стратегические закупки\" - Центр Логистики (2023)\n• \"Переговоры с поставщиками\" - Business Training (2022)\n• \"Управление запасами\" - Supply Chain Academy (2021)','350000','Путешествия, коллекционирование монет, настольный теннис','Закупочная деятельность, работа с поставщиками, складской учет, ценообразование, ведение переговоров','','Алматы, Казахстан','','','Положительные отзывы от поставщиков и руководства компании','','',0),(17,'pbkdf2_sha256$870000$2Baux4JCzIjPvO4KOiLX18$GeDEbEyBwBcpb2A/gqCTxaa198URDqxNWffEPr6D6t0=',NULL,0,'aset.ilyamov','Асет','Ильямов',0,1,'2025-05-30 10:53:50.177850','aset.ilyamov@barlau.org','+77771234573','TECH',0,NULL,NULL,NULL,NULL,'Главный механик','2005-2025: Главный механик ТОО \"Barlau\" - Ремонт и обслуживание автопарка\r\n2000-2005: Слесарь-механик ООО \"АвтоСервис\" - Ремонт грузовых автомобилей','Алматинский автодорожный техникум, специальность \"Ремонт и обслуживание автомобилей\" (1990-1995). Множественные курсы по новым технологиям.','','employee_photos/9.png','Удостоверение автомеханика 6 разряда, Сертификат по сварочным работам\r\n\r\n• Освоил ремонт всех марок грузовиков в автопарке\r\n• Сократил время ремонта в среднем на 25%\r\n• Обучил 10+ молодых механиков\r\n• Получил звание \"Мастер золотые руки\" (2019)','Казахский (родной), Русский (свободно)','Главный механик с многолетним опытом ремонта и обслуживания грузового автотранспорта. Поддерживаю техническое состояние автопарка на высоком уровне.','• Освоил ремонт всех марок грузовиков в автопарке\n• Сократил время ремонта в среднем на 25%\n• Обучил 10+ молодых механиков\n• Получил звание \"Мастер золотые руки\" (2019)',40,'• \"Ремонт современных дизельных двигателей\" - Caterpillar (2023)\n• \"Диагностика электронных систем\" - Bosch (2022)\n• \"Ремонт гидравлических систем\" - Parker Hannifin (2021)','400000','Ремонт автомобилей, рыбалка, слесарное дело, изобретательство','Диагностика автомобилей, ремонт двигателей, электрооборудование, гидравлика, сварочные работы','','Алматы, Казахстан','','','Рекомендации от водителей и технических специалистов отрасли','','',0),(18,'pbkdf2_sha256$870000$14llq7QHizNro9msgxH88f$uEY/agES2SdUjf4YrJg1EfMgGFyTuZIRq49nDFRyLQY=',NULL,0,'muratjan.ilakhunov','Муратжан','Илахунов',0,1,'2025-05-30 10:53:50.900477','muratjan.ilakhunov@barlau.org','+77771234574','CONSULTANT',0,NULL,NULL,NULL,NULL,'Внештатный консультант','2020-2025: Внештатный консультант ТОО \"Barlau\" - Консультирование по развитию бизнеса\r\n2015-2020: Директор ООО \"ТрансКонсалт\" - Консалтинговые услуги в сфере логистики\r\n','КазНУ им. аль-Фараби, экономический факультет (1990-1995). Executive MBA в области транспорта и логистики (2010-2012).','','employee_photos/8.png','Сертификат бизнес-консультанта международного уровня, Сертификат по управлению изменениями\r\n• Помог 15+ компаниям увеличить прибыльность\r\n• Разработал стратегию развития для крупных логистических компаний\r\n','Казахский (родной), Русский (свободно), Английский (продвинутый), Немецкий (средний)','Внештатный консультант с 20-летним опытом в транспортной отрасли. Специализируюсь на развитии бизнеса и стратегическом планировании.','• Помог 15+ компаниям увеличить прибыльность\n• Разработал стратегию развития для крупных логистических компаний\n• Провел успешную реструктуризацию 3 транспортных предприятий\n• Автор методики оптимизации логистических процессов',50,'• \"Цифровая трансформация логистики\" - Stanford (2023)\n• \"Лидерство в изменениях\" - Harvard Business School (2022)\n• \"Стратегический менеджмент\" - Wharton School (2021)','500000','Чтение бизнес-литературы, горные лыжи, игра на домбре, путешествия','Бизнес-консультирование, стратегическое планирование, анализ рынка, управление изменениями, развитие бизнеса','','Алматы, Казахстан','','Книга \"Логистика будущего\" (2022), статьи в профессиональных журналах','Рекомендательные письма от руководителей крупных транспортных компаний Казахстана','','',0),(19,'pbkdf2_sha256$870000$saRxS2C3TqRVNmdjX17hSO$pzBKgGEfGW5SHVxVCGpjeRhNG9xf/PaiGhS486IJMhY=',NULL,0,'aidana.uzakova','Айдана','Узакова',0,1,'2025-05-30 10:53:51.608733','aidana.uzakova@barlau.org','+77771234575','LOGIST',0,NULL,NULL,NULL,NULL,'Логист / Офис-менеджер','2017-2025: Логист / Офис-менеджер ТОО \"Barlau\" - Планирование маршрутов, документооборот\r\n2014-2017: Специалист по логистике ООО \"КаргоКЗ\" - Обработка заявок на перевозки\r\n2012-2014: Секретарь-референт ТОО \"БизнесЦентр\" - Административная работа','Казахстанско-Британский технический университет, факультет менеджмента (2008-2012). Дополнительное образование по логистике и управлению офисом.','','employee_photos/7.png','','Казахский (родной), Русский (свободно), Английский (средний), Корейский (базовый)','Логист и офис-менеджер, отвечаю за планирование перевозок и организацию офисной работы. Стремлюсь к максимальной эффективности всех процессов.','• Оптимизировала процесс обработки заявок (сокращение времени на 40%)\n• Внедрила электронный документооборот\n• Организовала эффективную систему архивирования\n• Улучшила коммуникацию между отделами',26,'• \"Эффективная логистика\" - Международная Академия Логистики (2023)\n• \"Управление офисом\" - Business Skills Academy (2022)\n• \"Тайм-менеджмент и организация работы\" - Time Management Institute (2021)','300000','Йога, чтение, изучение языков, организация мероприятий','Логистическое планирование, документооборот, организация работы офиса, координация, многозадачность','','Алматы, Казахстан','','','Положительные отзывы от коллег и клиентов компании','','',0),(20,'pbkdf2_sha256$870000$Aj5lrkGZCC3SbTGGQ6B4o6$JErLQHIrbKEAQJ7TOP0vTg9Ivd4290kgG7/+Y4NsDvo=','2025-05-30 20:21:10.263848',0,'yunus','Юнус','Алиев',0,1,'2025-05-30 12:33:44.666271','yunus@gmail.com','+7 (777) 159 03 06','DRIVER',0,NULL,NULL,NULL,NULL,'Водитель','','','','','','','','',NULL,'','','','','','','','','','','',0),(21,'pbkdf2_sha256$870000$iL2eg7N5F6Nl5VBX9ws67K$h06IGoOCwEM0C2qS6M/PSy90mbZyDwY12ejo8089Dq0=',NULL,0,'arman','Арман','Вадиев',0,1,'2025-05-30 12:34:19.538574','arman@gmail.com','','DRIVER',0,NULL,NULL,NULL,NULL,'Водитель','','','','','','','','',NULL,'','','','','','','','','','','',0),(22,'pbkdf2_sha256$870000$hX20t0EaO5ser8O9KosJ9a$m0D+owU27DLKc+qSrS2RfdqYZfrSj3JrVrRroCP4Y/I=','2025-06-18 11:13:01.405747',0,'ruslan','Руслан','Алимкулов',0,1,'2025-05-30 14:34:12.420841','ruslan@barlau.org','+77024240392','DIRECTOR',0,NULL,NULL,NULL,NULL,'','','','','','','','','',NULL,'','','','','','','','','','','',0);
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Уведомление',6,'add_notification'),(22,'Can change Уведомление',6,'change_notification'),(23,'Can delete Уведомление',6,'delete_notification'),(24,'Can view Уведомление',6,'view_notification'),(25,'Can add Путевой лист',7,'add_waybill'),(26,'Can change Путевой лист',7,'change_waybill'),(27,'Can delete Путевой лист',7,'delete_waybill'),(28,'Can view Путевой лист',7,'view_waybill'),(29,'Can add Пользователь',8,'add_user'),(30,'Can change Пользователь',8,'change_user'),(31,'Can delete Пользователь',8,'delete_user'),(32,'Can view Пользователь',8,'view_user'),(33,'Can add Пользователь',9,'add_user'),(34,'Can change Пользователь',9,'change_user'),(35,'Can delete Пользователь',9,'delete_user'),(36,'Can view Пользователь',9,'view_user'),(37,'Can add Транспортное средство',10,'add_vehicle'),(38,'Can change Транспортное средство',10,'change_vehicle'),(39,'Can delete Транспортное средство',10,'delete_vehicle'),(40,'Can view Транспортное средство',10,'view_vehicle'),(41,'Can add Задача',11,'add_task'),(42,'Can change Задача',11,'change_task'),(43,'Can delete Задача',11,'delete_task'),(44,'Can view Задача',11,'view_task'),(45,'Can add Расход',12,'add_expense'),(46,'Can change Расход',12,'change_expense'),(47,'Can delete Расход',12,'delete_expense'),(48,'Can view Расход',12,'view_expense'),(49,'Can add Путевой лист',13,'add_waybilldocument'),(50,'Can change Путевой лист',13,'change_waybilldocument'),(51,'Can delete Путевой лист',13,'delete_waybilldocument'),(52,'Can view Путевой лист',13,'view_waybilldocument'),(53,'Can add Поездка',14,'add_trip'),(54,'Can change Поездка',14,'change_trip'),(55,'Can delete Поездка',14,'delete_trip'),(56,'Can view Поездка',14,'view_trip'),(57,'Can add Геолокация водителя',15,'add_driverlocation'),(58,'Can change Геолокация водителя',15,'change_driverlocation'),(59,'Can delete Геолокация водителя',15,'delete_driverlocation'),(60,'Can view Геолокация водителя',15,'view_driverlocation'),(61,'Can add Документ транспорта',16,'add_vehicledocument'),(62,'Can change Документ транспорта',16,'change_vehicledocument'),(63,'Can delete Документ транспорта',16,'delete_vehicledocument'),(64,'Can view Документ транспорта',16,'view_vehicledocument'),(65,'Can add Техническое обслуживание',17,'add_vehiclemaintenance'),(66,'Can change Техническое обслуживание',17,'change_vehiclemaintenance'),(67,'Can delete Техническое обслуживание',17,'delete_vehiclemaintenance'),(68,'Can view Техническое обслуживание',17,'view_vehiclemaintenance'),(69,'Can add Фотография транспорта',18,'add_vehiclephoto'),(70,'Can change Фотография транспорта',18,'change_vehiclephoto'),(71,'Can delete Фотография транспорта',18,'delete_vehiclephoto'),(72,'Can view Фотография транспорта',18,'view_vehiclephoto');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_driverlocation`
--

DROP TABLE IF EXISTS `core_driverlocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_driverlocation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `latitude` decimal(18,15) NOT NULL,
  `longitude` decimal(18,15) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `driver_id` bigint NOT NULL,
  `trip_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_driverlocation_driver_id_idx` (`driver_id`),
  KEY `core_driverlocation_trip_id_idx` (`trip_id`),
  CONSTRAINT `core_driverlocation_driver_id_fk` FOREIGN KEY (`driver_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `core_driverlocation_trip_id_fk` FOREIGN KEY (`trip_id`) REFERENCES `core_trip` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=296 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_driverlocation`
--

LOCK TABLES `core_driverlocation` WRITE;
/*!40000 ALTER TABLE `core_driverlocation` DISABLE KEYS */;
INSERT INTO `core_driverlocation` VALUES (76,51.086163100000000,71.430624500000000,'2025-05-30 14:48:11.585561',20,NULL),(77,51.086164400000000,71.430608300000000,'2025-05-30 14:48:17.492658',20,NULL),(78,51.086157000000000,71.430655000000000,'2025-05-30 14:48:24.574848',20,NULL),(79,51.086157000000000,71.430655000000000,'2025-05-30 14:48:24.578411',20,NULL),(80,51.086148500000000,71.430654200000000,'2025-05-30 14:48:27.069739',20,NULL),(81,51.086147100000000,71.430651200000000,'2025-05-30 14:48:31.927013',20,NULL),(82,51.086094100000000,71.430631500000000,'2025-05-30 14:48:36.098445',20,NULL),(83,51.086094100000000,71.430631500000000,'2025-05-30 14:48:36.100382',20,NULL),(84,51.086093900000000,71.430616500000000,'2025-05-30 14:48:41.007324',20,NULL),(85,51.086030600000000,71.430586000000000,'2025-05-30 14:48:44.069058',20,NULL),(86,51.086030600000000,71.430586000000000,'2025-05-30 14:48:44.547940',20,NULL),(87,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.001033',20,NULL),(88,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.006231',20,NULL),(89,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.006668',20,NULL),(90,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.062771',20,NULL),(91,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.066078',20,NULL),(92,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.067225',20,NULL),(93,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.083869',20,NULL),(94,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.166274',20,NULL),(95,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.166653',20,NULL),(96,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.172444',20,NULL),(97,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.190445',20,NULL),(98,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.197343',20,NULL),(99,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.202155',20,NULL),(100,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.213225',20,NULL),(101,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.221162',20,NULL),(102,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.230357',20,NULL),(103,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.243726',20,NULL),(104,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.245539',20,NULL),(105,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.268564',20,NULL),(106,51.086164100000000,71.430638100000000,'2025-05-30 14:49:50.281757',20,NULL),(107,51.085911311472340,71.430567657409770,'2025-05-30 14:51:09.150056',20,NULL),(108,51.085912861512530,71.430573867206490,'2025-05-30 14:51:12.134723',20,NULL),(109,51.085912861512530,71.430573867206490,'2025-05-30 14:51:15.171895',20,NULL),(110,51.085912861512530,71.430573867206490,'2025-05-30 14:51:18.141510',20,NULL),(111,51.085912861512530,71.430573867206490,'2025-05-30 14:51:21.144022',20,NULL),(112,51.085901209750870,71.430551341969690,'2025-05-30 14:51:24.151139',20,NULL),(113,51.085901209750870,71.430551341969690,'2025-05-30 14:51:27.151815',20,NULL),(114,51.085901209750870,71.430551341969690,'2025-05-30 14:51:30.132674',20,NULL),(115,51.085901209750870,71.430551341969690,'2025-05-30 14:51:33.143268',20,NULL),(116,51.085900473047310,71.430550409484850,'2025-05-30 14:51:36.145287',20,NULL),(117,51.085900473047310,71.430550409484850,'2025-05-30 14:51:39.137791',20,NULL),(118,51.085900473047310,71.430550409484850,'2025-05-30 14:51:42.162623',20,NULL),(119,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.273521',20,NULL),(120,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.287794',20,NULL),(121,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.368467',20,NULL),(122,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.386004',20,NULL),(123,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.389661',20,NULL),(124,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.448310',20,NULL),(125,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.497165',20,NULL),(126,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.503927',20,NULL),(127,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.505021',20,NULL),(128,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.517774',20,NULL),(129,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.527743',20,NULL),(130,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.551112',20,NULL),(131,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.627042',20,NULL),(132,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.627420',20,NULL),(133,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.631539',20,NULL),(134,51.085898637533305,71.430586225560860,'2025-05-30 14:52:32.653766',20,NULL),(135,51.085898637533305,71.430586225560860,'2025-05-30 14:52:33.169791',20,NULL),(136,51.085898518419505,71.430588898741620,'2025-05-30 14:52:38.386337',20,NULL),(137,51.085898518419505,71.430588898741620,'2025-05-30 14:52:41.401020',20,NULL),(138,51.085898518419505,71.430588898741620,'2025-05-30 14:52:44.375424',20,NULL),(139,51.085898518419505,71.430588898741620,'2025-05-30 14:52:47.347811',20,NULL),(140,51.085912185206600,71.430586377984500,'2025-05-30 14:52:50.487310',20,NULL),(141,51.085912185206600,71.430586377984500,'2025-05-30 14:52:53.335741',20,NULL),(142,51.085912185206600,71.430586377984500,'2025-05-30 14:52:56.392628',20,NULL),(143,51.085912185206600,71.430586377984500,'2025-05-30 14:52:59.356054',20,NULL),(144,51.085912185206600,71.430586377984500,'2025-05-30 14:53:02.369763',20,NULL),(145,51.085927073341864,71.430580325660420,'2025-05-30 14:53:05.396851',20,NULL),(146,51.085927073341864,71.430580325660420,'2025-05-30 14:53:08.347553',20,NULL),(147,51.085927073341864,71.430580325660420,'2025-05-30 14:53:11.336893',20,NULL),(148,51.085927073341864,71.430580325660420,'2025-05-30 14:53:14.392732',20,NULL),(149,51.085929613782850,71.430563686277180,'2025-05-30 14:53:17.358716',20,NULL),(150,51.085929613782850,71.430563686277180,'2025-05-30 14:54:35.856469',20,NULL),(151,51.085929613782850,71.430563686277180,'2025-05-30 14:54:35.870512',20,NULL),(152,51.085929613782850,71.430563686277180,'2025-05-30 14:54:35.871357',20,NULL),(153,51.085929613782850,71.430563686277180,'2025-05-30 14:54:35.958051',20,NULL),(154,51.085929613782850,71.430563686277180,'2025-05-30 14:54:35.966436',20,NULL),(155,51.085929613782850,71.430563686277180,'2025-05-30 14:54:35.968187',20,NULL),(156,51.085929613782850,71.430563686277180,'2025-05-30 14:54:35.978446',20,NULL),(157,51.085929613782850,71.430563686277180,'2025-05-30 14:54:35.993619',20,NULL),(158,51.085929613782850,71.430563686277180,'2025-05-30 14:54:35.997953',20,NULL),(159,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.014817',20,NULL),(160,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.024459',20,NULL),(161,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.028218',20,NULL),(162,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.040524',20,NULL),(163,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.056677',20,NULL),(164,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.062789',20,NULL),(165,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.081467',20,NULL),(166,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.088148',20,NULL),(167,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.095562',20,NULL),(168,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.123125',20,NULL),(169,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.129950',20,NULL),(170,51.085929613782850,71.430563686277180,'2025-05-30 14:54:36.134403',20,NULL),(171,51.085942631167654,71.430575555292420,'2025-05-30 14:54:38.356855',20,NULL),(172,51.085942631167654,71.430575555292420,'2025-05-30 14:54:41.372478',20,NULL),(173,51.085921759550580,71.430636036375320,'2025-05-30 14:54:44.342167',20,NULL),(174,51.086164100000000,71.430638100000000,'2025-05-30 14:54:45.712396',20,NULL),(175,51.085921759550580,71.430636036375320,'2025-05-30 14:54:47.358780',20,NULL),(176,51.085921759550580,71.430636036375320,'2025-05-30 14:54:50.338279',20,NULL),(177,51.085921759550580,71.430636036375320,'2025-05-30 14:54:53.334360',20,NULL),(178,51.085919286473990,71.430628587656300,'2025-05-30 14:54:56.343161',20,NULL),(179,51.085919286473990,71.430628587656300,'2025-05-30 14:54:59.354828',20,NULL),(180,51.085919286473990,71.430628587656300,'2025-05-30 14:55:02.333475',20,NULL),(181,51.085919286473990,71.430628587656300,'2025-05-30 14:55:05.348106',20,NULL),(182,51.085934923282430,71.430628244931900,'2025-05-30 14:55:08.337673',20,NULL),(183,51.085934923282430,71.430628244931900,'2025-05-30 14:55:11.343278',20,NULL),(184,51.085934923282430,71.430628244931900,'2025-05-30 14:55:14.357973',20,NULL),(185,51.085934923282430,71.430628244931900,'2025-05-30 14:55:17.373812',20,NULL),(186,51.085920154967260,71.430628145440080,'2025-05-30 14:55:20.344669',20,NULL),(187,51.085920154967260,71.430628145440080,'2025-05-30 14:55:23.348588',20,NULL),(188,51.085920154967260,71.430628145440080,'2025-05-30 14:55:26.338035',20,NULL),(189,51.085920154967260,71.430628145440080,'2025-05-30 14:55:29.348116',20,NULL),(190,51.085910170616940,71.430585560485430,'2025-05-30 14:55:32.392356',20,NULL),(191,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.487012',20,NULL),(192,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.624485',20,NULL),(193,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.632984',20,NULL),(194,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.759300',20,NULL),(195,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.762501',20,NULL),(196,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.792461',20,NULL),(197,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.798867',20,NULL),(198,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.835306',20,NULL),(199,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.841085',20,NULL),(200,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.860620',20,NULL),(201,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.900819',20,NULL),(202,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.920516',20,NULL),(203,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.931021',20,NULL),(204,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.949812',20,NULL),(205,51.085910170616940,71.430585560485430,'2025-05-30 15:09:00.963687',20,NULL),(206,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.010891',20,NULL),(207,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.016785',20,NULL),(208,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.058376',20,NULL),(209,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.061247',20,NULL),(210,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.104418',20,NULL),(211,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.108327',20,NULL),(212,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.148594',20,NULL),(213,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.150876',20,NULL),(214,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.177143',20,NULL),(215,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.202782',20,NULL),(216,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.209477',20,NULL),(217,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.228647',20,NULL),(218,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.241441',20,NULL),(219,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.261426',20,NULL),(220,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.278198',20,NULL),(221,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.315485',20,NULL),(222,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.402664',20,NULL),(223,51.085910170616940,71.430585560485430,'2025-05-30 15:09:01.402389',20,NULL),(224,51.085896466380690,71.430595193282260,'2025-05-30 15:09:02.371119',20,NULL),(225,51.085908956761880,71.430593548017240,'2025-05-30 15:09:16.366949',20,NULL),(226,51.085908956761880,71.430593548017240,'2025-05-30 15:09:16.369378',20,NULL),(227,51.085908956761880,71.430593548017240,'2025-05-30 15:09:16.382460',20,NULL),(228,51.085908956761880,71.430593548017240,'2025-05-30 15:09:16.390491',20,NULL),(229,51.085908956761880,71.430593548017240,'2025-05-30 15:09:17.362206',20,NULL),(230,51.085920031712900,71.430608071959410,'2025-05-30 15:23:33.601329',20,NULL),(231,51.085920031712900,71.430608071959410,'2025-05-30 15:23:36.626380',20,NULL),(232,51.085920031712900,71.430608071959410,'2025-05-30 15:23:39.634746',20,NULL),(233,51.085920031712900,71.430608071959410,'2025-05-30 15:23:42.655198',20,NULL),(234,51.085920249941790,71.430608937129830,'2025-05-30 15:23:45.636446',20,NULL),(235,51.085920249941790,71.430608937129830,'2025-05-30 15:23:48.602450',20,NULL),(236,51.085920249941790,71.430608937129830,'2025-05-30 15:23:51.629409',20,NULL),(237,51.085920249941790,71.430608937129830,'2025-05-30 15:23:54.589634',20,NULL),(238,51.085928613082550,71.430592538186290,'2025-05-30 15:23:57.613893',20,NULL),(239,51.085928613082550,71.430592538186290,'2025-05-30 15:24:00.621502',20,NULL),(240,51.085928613082550,71.430592538186290,'2025-05-30 15:24:03.585048',20,NULL),(241,51.085928613082550,71.430592538186290,'2025-05-30 15:24:06.584139',20,NULL),(242,51.085934912512830,71.430600134035840,'2025-05-30 15:24:09.614635',20,NULL),(243,51.085934912512830,71.430600134035840,'2025-05-30 15:24:12.625997',20,NULL),(244,51.085934912512830,71.430600134035840,'2025-05-30 15:24:15.612780',20,NULL),(245,51.085934912512830,71.430600134035840,'2025-05-30 15:24:18.600065',20,NULL),(246,51.085968209558814,71.430600224006450,'2025-05-30 15:24:21.602746',20,NULL),(247,51.085968209558814,71.430600224006450,'2025-05-30 15:24:24.609607',20,NULL),(248,51.085968209558814,71.430600224006450,'2025-05-30 15:24:27.618367',20,NULL),(249,51.085968209558814,71.430600224006450,'2025-05-30 15:24:30.610692',20,NULL),(250,51.085933041141660,71.430620501063570,'2025-05-30 15:26:33.311052',20,NULL),(251,51.085933041141660,71.430620501063570,'2025-05-30 15:26:33.311987',20,NULL),(252,51.085933041141660,71.430620501063570,'2025-05-30 15:26:34.496888',20,NULL),(253,51.085933041141660,71.430620501063570,'2025-05-30 15:26:34.710431',20,NULL),(254,51.085933041141660,71.430620501063570,'2025-05-30 15:26:34.710933',20,NULL),(255,51.085933041141660,71.430620501063570,'2025-05-30 15:26:35.687756',20,NULL),(256,51.085933041141660,71.430620501063570,'2025-05-30 15:26:35.748743',20,NULL),(257,51.085933041141660,71.430620501063570,'2025-05-30 15:26:35.749941',20,NULL),(258,51.085933041141660,71.430620501063570,'2025-05-30 15:26:36.179604',20,NULL),(259,51.085933041141660,71.430620501063570,'2025-05-30 15:26:36.581090',20,NULL),(260,51.085933041141660,71.430620501063570,'2025-05-30 15:26:36.585293',20,NULL),(261,51.085933041141660,71.430620501063570,'2025-05-30 15:26:36.686466',20,NULL),(262,51.085933041141660,71.430620501063570,'2025-05-30 15:26:36.752479',20,NULL),(263,51.085933041141660,71.430620501063570,'2025-05-30 15:26:37.188890',20,NULL),(264,51.085933041141660,71.430620501063570,'2025-05-30 15:26:37.188926',20,NULL),(265,51.085933041141660,71.430620501063570,'2025-05-30 15:26:37.368116',20,NULL),(266,51.085933041141660,71.430620501063570,'2025-05-30 15:26:37.368182',20,NULL),(267,51.085933041141660,71.430620501063570,'2025-05-30 15:26:38.532220',20,NULL),(268,51.085933041141660,71.430620501063570,'2025-05-30 15:26:38.534722',20,NULL),(269,51.085933041141660,71.430620501063570,'2025-05-30 15:26:38.686182',20,NULL),(270,51.085933041141660,71.430620501063570,'2025-05-30 15:26:38.710130',20,NULL),(271,51.085933041141660,71.430620501063570,'2025-05-30 15:26:40.290345',20,NULL),(272,51.085933041141660,71.430620501063570,'2025-05-30 15:26:40.291391',20,NULL),(273,51.085933041141660,71.430620501063570,'2025-05-30 15:26:40.294390',20,NULL),(274,51.085933041141660,71.430620501063570,'2025-05-30 15:26:40.318925',20,NULL),(275,51.085933041141660,71.430620501063570,'2025-05-30 15:26:42.582764',20,NULL),(276,51.085910963947360,71.430623818600550,'2025-05-30 15:26:45.578083',20,NULL),(277,51.085910963947360,71.430623818600550,'2025-05-30 15:26:48.577433',20,NULL),(278,51.085910963947360,71.430623818600550,'2025-05-30 15:26:51.579955',20,NULL),(279,51.085910963947360,71.430623818600550,'2025-05-30 15:26:54.590780',20,NULL),(280,51.085908138420834,71.430623275853430,'2025-05-30 15:26:57.582630',20,NULL),(281,51.085908138420834,71.430623275853430,'2025-05-30 15:27:00.580405',20,NULL),(282,51.085908138420834,71.430623275853430,'2025-05-30 15:27:03.583429',20,NULL),(283,51.085908138420834,71.430623275853430,'2025-05-30 15:27:06.577068',20,NULL),(284,51.085888264741044,71.430575205946110,'2025-05-30 15:27:09.639596',20,NULL),(285,51.085888264741044,71.430575205946110,'2025-05-30 15:27:12.591240',20,NULL),(286,51.134094054458025,71.436961052017750,'2025-05-30 20:21:15.136992',20,NULL),(287,51.134188538822684,71.437019099152900,'2025-05-30 20:21:18.118620',20,NULL),(288,51.134186378651160,71.437018698616670,'2025-05-30 20:21:21.173108',20,NULL),(289,51.134226982425480,71.437002707889900,'2025-05-30 20:21:24.081664',20,NULL),(290,51.134224034813386,71.437001545019480,'2025-05-30 20:21:27.174589',20,NULL),(291,51.134084280188084,71.436907851252460,'2025-05-30 20:21:30.090354',20,NULL),(292,51.134049292455000,71.436887246439640,'2025-05-30 20:21:33.174794',20,NULL),(293,51.134146310565530,71.437125090830250,'2025-05-30 20:21:36.184287',20,NULL),(294,51.134152318603680,71.437127937004380,'2025-05-30 20:21:39.173436',20,NULL),(295,51.134225270761610,71.437009905486010,'2025-05-30 20:21:42.150248',20,NULL);
/*!40000 ALTER TABLE `core_driverlocation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_notification`
--

DROP TABLE IF EXISTS `core_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `link` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_notification_user_id_6e341aac_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `core_notification_user_id_6e341aac_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_notification`
--

LOCK TABLES `core_notification` WRITE;
/*!40000 ALTER TABLE `core_notification` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_trip`
--

DROP TABLE IF EXISTS `core_trip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_trip` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_latitude` decimal(9,6) NOT NULL,
  `start_longitude` decimal(9,6) NOT NULL,
  `end_latitude` decimal(9,6) NOT NULL,
  `end_longitude` decimal(9,6) NOT NULL,
  `start_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `end_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `cargo_description` longtext COLLATE utf8mb4_unicode_ci,
  `date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `driver_id` bigint NOT NULL,
  `vehicle_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_trip_driver_id_idx` (`driver_id`),
  KEY `core_trip_vehicle_id_idx` (`vehicle_id`),
  CONSTRAINT `core_trip_driver_id_fk` FOREIGN KEY (`driver_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `core_trip_vehicle_id_fk` FOREIGN KEY (`vehicle_id`) REFERENCES `logistics_vehicle` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_trip`
--

LOCK TABLES `core_trip` WRITE;
/*!40000 ALTER TABLE `core_trip` DISABLE KEYS */;
INSERT INTO `core_trip` VALUES (8,44.165665,80.002739,44.211865,80.402995,'Жаркент, Панфиловский район, Жетысуская область, Казахстан','Хоргос, Yaouxilu, Коргас, Или, Синьцзян, Китай','Поездка за товаром','2025-05-31','2025-05-30 12:35:12.274585',21,29),(9,44.211865,80.402995,51.115993,71.467706,'Хоргос, Yaouxilu, Коргас, Или, Синьцзян, Китай','Астана, Казахстан','5 товаров от китайцев','2025-05-31','2025-05-30 12:35:58.018414',20,25);
/*!40000 ALTER TABLE `core_trip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user`
--

DROP TABLE IF EXISTS `core_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(17) COLLATE utf8mb4_unicode_ci NOT NULL,
  `position` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `photo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `current_latitude` decimal(9,6) DEFAULT NULL,
  `current_longitude` decimal(9,6) DEFAULT NULL,
  `last_location_update` datetime(6) DEFAULT NULL,
  `location_tracking_enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user`
--

LOCK TABLES `core_user` WRITE;
/*!40000 ALTER TABLE `core_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_groups`
--

DROP TABLE IF EXISTS `core_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`),
  CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_groups`
--

LOCK TABLES `core_user_groups` WRITE;
/*!40000 ALTER TABLE `core_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_user_user_permissions`
--

DROP TABLE IF EXISTS `core_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`),
  CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_user_user_permissions`
--

LOCK TABLES `core_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `core_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_waybill`
--

DROP TABLE IF EXISTS `core_waybill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_waybill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `departure_point` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `destination_point` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cargo_description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `cargo_weight` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `driver_id` bigint NOT NULL,
  `vehicle_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `core_waybill_created_by_id_aa832033_fk_accounts_user_id` (`created_by_id`),
  KEY `core_waybill_driver_id_5df6a151_fk_accounts_user_id` (`driver_id`),
  KEY `core_waybill_vehicle_id_d3093c18_fk_logistics_vehicle_id` (`vehicle_id`),
  CONSTRAINT `core_waybill_created_by_id_aa832033_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `core_waybill_driver_id_5df6a151_fk_accounts_user_id` FOREIGN KEY (`driver_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `core_waybill_vehicle_id_d3093c18_fk_logistics_vehicle_id` FOREIGN KEY (`vehicle_id`) REFERENCES `logistics_vehicle` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_waybill`
--

LOCK TABLES `core_waybill` WRITE;
/*!40000 ALTER TABLE `core_waybill` DISABLE KEYS */;
/*!40000 ALTER TABLE `core_waybill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'accounts','user'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(15,'core','driverlocation'),(6,'core','notification'),(14,'core','trip'),(8,'core','user'),(7,'core','waybill'),(12,'logistics','expense'),(11,'logistics','task'),(10,'logistics','vehicle'),(16,'logistics','vehicledocument'),(17,'logistics','vehiclemaintenance'),(18,'logistics','vehiclephoto'),(13,'logistics','waybilldocument'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-05-28 10:02:43.150949'),(2,'contenttypes','0002_remove_content_type_name','2025-05-28 10:02:43.329113'),(3,'auth','0001_initial','2025-05-28 10:02:44.099653'),(4,'auth','0002_alter_permission_name_max_length','2025-05-28 10:02:44.230947'),(5,'auth','0003_alter_user_email_max_length','2025-05-28 10:02:44.241896'),(6,'auth','0004_alter_user_username_opts','2025-05-28 10:02:44.252929'),(7,'auth','0005_alter_user_last_login_null','2025-05-28 10:02:44.265088'),(8,'auth','0006_require_contenttypes_0002','2025-05-28 10:02:44.272513'),(9,'auth','0007_alter_validators_add_error_messages','2025-05-28 10:02:44.283678'),(10,'auth','0008_alter_user_username_max_length','2025-05-28 10:02:44.293964'),(11,'auth','0009_alter_user_last_name_max_length','2025-05-28 10:02:44.304987'),(12,'auth','0010_alter_group_name_max_length','2025-05-28 10:02:44.331850'),(13,'auth','0011_update_proxy_permissions','2025-05-28 10:02:44.344573'),(14,'auth','0012_alter_user_first_name_max_length','2025-05-28 10:02:44.357036'),(15,'accounts','0001_initial','2025-05-28 10:02:45.221684'),(16,'accounts','0002_alter_user_options_alter_user_email_and_more','2025-05-28 10:02:45.565655'),(17,'accounts','0003_user_certifications_user_languages_and_more','2025-05-28 10:02:46.044771'),(18,'accounts','0004_user_about_me_user_achievements_user_age_and_more','2025-05-28 10:02:48.504838'),(19,'accounts','0005_user_recommendation_file','2025-05-28 10:02:48.649361'),(20,'accounts','0006_user_is_archived','2025-05-28 10:02:48.819614'),(21,'admin','0001_initial','2025-05-28 10:02:49.131674'),(22,'admin','0002_logentry_remove_auto_add','2025-05-28 10:02:49.147927'),(23,'admin','0003_logentry_add_action_flag_choices','2025-05-28 10:02:49.163555'),(34,'sessions','0001_initial','2025-05-28 10:02:55.506619'),(35,'logistics','0001_initial','2025-05-28 14:42:13.871357'),(36,'logistics','0002_alter_task_options_rename_deadline_task_due_date_and_more','2025-05-28 14:42:13.880895'),(37,'logistics','0003_vehicle_status_vehicle_vehicle_type','2025-05-28 14:42:13.890109'),(38,'logistics','0004_vehicle_cargo_capacity_vehicle_chassis_number_and_more','2025-05-28 14:42:13.902735'),(39,'logistics','0005_auto_20250503_1402','2025-05-28 14:42:13.917260'),(40,'logistics','0006_remove_vehiclemaintenance_created_by_and_more','2025-05-28 14:42:13.925597'),(41,'logistics','0007_vehicle_cargo_capacity_vehicle_chassis_number_and_more','2025-05-28 14:42:13.943738'),(42,'logistics','0008_remove_vehiclemaintenance_created_by_and_more','2025-05-28 14:42:13.951928'),(43,'logistics','0009_vehicle_cargo_capacity_vehicle_chassis_number_and_more','2025-05-28 14:42:13.961334'),(44,'logistics','0010_vehicle_color_vehicle_description_vehicle_main_photo','2025-05-28 14:42:13.971823'),(45,'logistics','0011_remove_vehicle_main_photo_vehicle_fuel_consumption','2025-05-28 14:42:13.986454'),(46,'logistics','0012_vehicle_is_archived','2025-05-28 14:42:13.995636'),(47,'logistics','0013_vehicle_main_photo','2025-05-28 14:42:14.010182'),(48,'logistics','0014_remove_vehicle_main_photo','2025-05-28 14:42:14.019321'),(49,'core','0001_initial','2025-05-28 14:42:14.029677'),(50,'core','0002_alter_driverlocation_latitude_and_more','2025-05-28 14:42:14.040364'),(51,'core','0003_alter_driverlocation_latitude_and_more','2025-05-28 14:42:14.048067'),(52,'accounts','0002_add_admin_role','2025-05-30 11:00:34.210074'),(53,'accounts','0003_alter_user_role','2025-05-30 11:00:34.244044');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3rsamcsexvno43k6wmbds9114nyak1ru','.eJxVi0sOwiAQQO_C2jR8y-DSE3gDMgzTQEwgEbpqvLs2caHb9zlExH2WuA9-xprFVWgpLr8wIT24nQaJ-t7mWE7JbVbCWXtb7qU3vn2zv7fgKJ_RJpmcsjY42DbvM0AIAQ1BNk5nJrWuKllGMslC8MEYByy1yYq1BMvi9QbtiTX5:1uL16c:HWHpHnSadYFFd3GabRBRCR3HmCtOMquld2xACO8uMts','2025-06-13 14:53:10.852935'),('42uqtyf0ds1dpinigi79w52xui1l4gls','.eJxVi00KQiEQgO_iOh4vf9Bp2Qm6gcyMI0qgkLqK7l4PWtT2-3mqiGuWuIY8Yk3qorRWp19IyHdph0Hmvtoc2yGlzco4a2_brfQm12_29xYc5TNaSwDnjAEYvcvaOqZkIIATChoNejIWQnJogLzoPYNLLI7CnlMyQb3eCxA3Ig:1uM3Ms:QhkAJTxcmbB8ZbMMJ6WpC7CgTqXP5eo_JXxukHbcQdw','2025-06-16 11:30:14.863641'),('ekervt0ma1bdqxaekdlbqb7ai3bpls48','.eJxVjE0OQiEQg-_C2rzIyK9LT-ANyLx5QyAmkAisjHcXEheartqv7UsEHD2F0fgZ8iGuAsTpN9uRHlwWQKI6Sm_bglx6Juy5lu2eauHbt_a3TdjSepQqamfJO2vA2500R38-FChjJJGdlshLtlOABpwyl6gjSj1noKV4fwDN0DYE:1uKI3f:ciLY0xgMPJX_Y-4tixJNL_0qFPQhMCnBD4axwkNxzRk','2025-06-11 14:47:07.131589'),('h6qt0x189aqs220xrybnhid2fpc574pr','.eJxVjE0OQiEQg-_C2rzIyK9LT-ANyLx5QyAmkAisjHcXEheartqv7UsEHD2F0fgZ8iGuAsTpN9uRHlwWQKI6Sm_bglx6Juy5lu2eauHbt_a3TdjSepQqamfJO2vA2500R38-FChjJJGdlshLtlOABpwyl6gjSj1noKV4fwDN0DYE:1uKI4O:uINZzjlWAMie2KHwPNm8gdlZSVJ_ljviUe7104Aona8','2025-06-11 14:47:52.656407'),('i4dhhnmh1n7mycdf2dgufde6qxqkyi13','.eJxVjE0OQiEQg-_C2rzIyK9LT-ANyLx5QyAmkAisjHcXEheartqv7UsEHD2F0fgZ8iGuAsTpN9uRHlwWQKI6Sm_bglx6Juy5lu2eauHbt_a3TdjSepQqamfJO2vA2500R38-FChjJJGdlshLtlOABpwyl6gjSj1noKV4fwDN0DYE:1uKI0r:FI5iKUc2trYXjhVUYGXsOZuJX5VJUInMsazEBIImPM0','2025-06-11 14:44:13.535632'),('iq780diekc7kpf4aw7ejq19p8am2i10s','.eJxVi0sOAiEQBe_C2kyG5u_SE3gD0kATiAkkAivj3Z1JXOjyvap6MY9rFr8GPX1N7Mo4Z5ffM2B8UDsJxthXm2M7IbVZI87a23YvvdHtq_21BUc5QqmJGzQhpZxhV5JAuWOKLKN2KGA3WgTIyQiejMpKg5Y2WUKb0Tng7P0BBhU2gg:1uQs61:2vNuNfC14UGyVvjcXbU5Xhs8zuzA_CYKfi4TisSsyRQ','2025-06-29 18:28:45.797595'),('kbbizzq98nsp8rglg23877e00y5z07at','.eJxVi0sOwiAQQO_C2jRAoQMuPYE3IMMwDcQEEgsr492liQvdvs9LBBw9h3HwM5QkrkKJyy-LSA-up0CiNmo_llNy7YWwl1aXe26Vb9_s78145DlKzxqU02aLnAgkWN726CEaXJONnqcyXjpJEtiCMmmNemK7a1LSafH-AM5jNeU:1uKEAz:Ht_3vUN1b0NLGPXmk2IImncX9O0dQNwDHEQ00owJ_rE','2025-06-11 10:38:25.189868'),('m64dq161zpajbj68s2v75mxw0mx82f75','.eJxVi0sOwiAQQO_C2jRAoQMuPYE3IMMwDcQEEgsr492liQvdvs9LBBw9h3HwM5QkrkKJyy-LSA-up0CiNmo_llNy7YWwl1aXe26Vb9_s78145DlKzxqU02aLnAgkWN726CEaXJONnqcyXjpJEtiCMmmNemK7a1LSafH-AM5jNeU:1uKEAf:tv7zx1w6JNq-yc0sO9L8wPl2i7jh5u2HVpOOYAQFih8','2025-06-11 10:38:05.228131'),('pb7l9pi4qdjte1oc08rv4ftlvcwqzja8','.eJxVjDEKQyEQBe9iHT77VVZNmRPkBrKuihJQiFqF3D0IKZJ2Zt57CU9rFr9GevoaxVWc4vLLAvEjtS2Iua82x7FlarMyzdrbcS-9pds3-9sWGmU_ZqlJY9ZAisHYhBmAtLGStITAhGdEzFEZa1k6m6OxEDSCchHQoXh_AMybNbA:1uL6B5:MHWQgl_yh9tdYuMRh3VpwmC2-ND53hzjxMAQVCz5klo','2025-06-13 20:18:07.096698'),('rif3m2cxhw6179lydzvhc7bup7irkic4','.eJxVi0sOAiEQBe_C2kyG5u_SE3gD0kATiAkkAivj3Z1JXOjyvap6MY9rFr8GPX1N7Mo4Z5ffM2B8UDsJxthXm2M7IbVZI87a23YvvdHtq_21BUc5QqmJGzQhpZxhV5JAuWOKLKN2KGA3WgTIyQiejMpKg5Y2WUKb0Tng7P0BBhU2gg:1uL453:JkB-0BXzjrYkvotABc2v86iEwwrnX4ps5r6neyb4l0M','2025-06-13 18:03:45.261326'),('v2xcfkmh0pdddf3yhawvsqpn77khe6m1','.eJxVi0sOAiEQBe_C2kyG5u_SE3gD0kATiAkkAivj3Z1JXOjyvap6MY9rFr8GPX1N7Mo4Z5ffM2B8UDsJxthXm2M7IbVZI87a23YvvdHtq_21BUc5QqmJGzQhpZxhV5JAuWOKLKN2KGA3WgTIyQiejMpKg5Y2WUKb0Tng7P0BBhU2gg:1uL1eG:gy1ktz371FA8dlOEz6jmKx2dj_KsXRdcOPYCesK-QJs','2025-06-13 15:27:56.521176'),('vckdhkwlnb8uhmofpkokk0plldx50snm','.eJxVi0sOwiAQQO_C2jR8y-DSE3gDMgzTQEwgEbpqvLs2caHb9zlExH2WuA9-xprFVWgpLr8wIT24nQaJ-t7mWE7JbVbCWXtb7qU3vn2zv7fgKJ_RJpmcsjY42DbvM0AIAQ1BNk5nJrWuKllGMslC8MEYByy1yYq1BMvi9QbtiTX5:1uL6E2:6UduCoPM2UKbKWxYEVZy7kz96no4do2e3WrxgDwv00o','2025-06-13 20:21:10.276080'),('vwow7lwk7ss13nmzks2wdoafxs6fj3or','.eJxVi00KQiEQgO_iOh4vf9Bp2Qm6gcyMI0qgkLqK7l4PWtT2-3mqiGuWuIY8Yk3qorRWp19IyHdph0Hmvtoc2yGlzco4a2_brfQm12_29xYc5TNaSwDnjAEYvcvaOqZkIIATChoNejIWQnJogLzoPYNLLI7CnlMyQb3eCxA3Ig:1uL6ea:48dyBiAeuE0PxZfjX9yuM_glMjRGsUHASjjlZNobN1w','2025-06-13 20:48:36.408946'),('y9r58967kkly26w6wo1j848lujjarcbt','.eJxVjE0OQiEQg-_C2rzIyK9LT-ANyLx5QyAmkAisjHcXEheartqv7UsEHD2F0fgZ8iGuAsTpN9uRHlwWQKI6Sm_bglx6Juy5lu2eauHbt_a3TdjSepQqamfJO2vA2500R38-FChjJJGdlshLtlOABpwyl6gjSj1noKV4fwDN0DYE:1uKI2t:RcFKWOtO9kOolpi7JbHlWMyA90xM1RplbGfSkhCdY0o','2025-06-11 14:46:19.379652'),('yi47plzm925gvdo70lxgm566l6mikdvb','.eJxVjE0OQiEQg-_C2rzIyK9LT-ANyLx5QyAmkAisjHcXEheartqv7UsEHD2F0fgZ8iGuAsTpN9uRHlwWQKI6Sm_bglx6Juy5lu2eauHbt_a3TdjSepQqamfJO2vA2500R38-FChjJJGdlshLtlOABpwyl6gjSj1noKV4fwDN0DYE:1uKHtx:BLKe9_FQgPvOXKUXq1PhS8BTBsQwbPNwXpMuXaO3b9s','2025-06-11 14:37:05.647304');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logistics_expense`
--

DROP TABLE IF EXISTS `logistics_expense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistics_expense` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `category` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `receipt` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_by_id` bigint NOT NULL,
  `vehicle_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `logistics_expense_created_by_id_758dc655_fk_accounts_user_id` (`created_by_id`),
  KEY `logistics_expense_vehicle_id_74b17986_fk_logistics_vehicle_id` (`vehicle_id`),
  CONSTRAINT `logistics_expense_created_by_id_758dc655_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `logistics_expense_vehicle_id_74b17986_fk_logistics_vehicle_id` FOREIGN KEY (`vehicle_id`) REFERENCES `logistics_vehicle` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistics_expense`
--

LOCK TABLES `logistics_expense` WRITE;
/*!40000 ALTER TABLE `logistics_expense` DISABLE KEYS */;
/*!40000 ALTER TABLE `logistics_expense` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logistics_task`
--

DROP TABLE IF EXISTS `logistics_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistics_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `due_date` datetime(6) NOT NULL,
  `assigned_to_id` bigint DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `vehicle_id` bigint DEFAULT NULL,
  `priority` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `logistics_task_vehicle_id_e9566045_fk_logistics_vehicle_id` (`vehicle_id`),
  KEY `logistics_task_assigned_to_id_f1aefc8f_fk_accounts_user_id` (`assigned_to_id`),
  KEY `logistics_task_created_by_id_1f7fb524_fk_accounts_user_id` (`created_by_id`),
  CONSTRAINT `logistics_task_assigned_to_id_f1aefc8f_fk_accounts_user_id` FOREIGN KEY (`assigned_to_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `logistics_task_created_by_id_1f7fb524_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `logistics_task_vehicle_id_e9566045_fk_logistics_vehicle_id` FOREIGN KEY (`vehicle_id`) REFERENCES `logistics_vehicle` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistics_task`
--

LOCK TABLES `logistics_task` WRITE;
/*!40000 ALTER TABLE `logistics_task` DISABLE KEYS */;
INSERT INTO `logistics_task` VALUES (1,'Доставка товаров в Шымкент','Перевозка строительных материалов по адресу: ул. Байтурсынова, 45','COMPLETED','2025-05-29 22:04:48.365223','2025-05-29 22:38:57.600118','2025-06-10 19:00:00.000000',NULL,NULL,NULL,'HIGH'),(2,'Погрузка в порту Актау','Забрать контейнеры с морского порта, доставить на склад','COMPLETED','2025-05-29 22:04:48.376965','2025-05-29 22:38:56.728092','2025-06-04 19:00:00.000000',NULL,NULL,NULL,'MEDIUM'),(3,'Транспортировка в Алматы','Доставка продукции на склад в Алматы, район Медеу','NEW','2025-05-29 22:04:48.387845','2025-05-30 18:06:15.763429','2025-05-31 07:00:00.000000',NULL,NULL,NULL,'LOW'),(4,'Экспресс доставка в Нур-Султан','Срочная доставка документов и образцов','NEW','2025-05-29 22:04:48.398038','2025-05-30 20:12:21.157504','2025-06-02 07:00:00.000000',NULL,NULL,NULL,'HIGH'),(6,'Сборный груз в Костанай','Забрать несколько мелких грузов, консолидировать и доставить','COMPLETED','2025-05-29 22:04:48.417372','2025-05-30 15:25:49.758267','2025-06-08 07:00:00.000000',NULL,NULL,NULL,'LOW'),(22,'Сдать отчет за май','Необходимо сдать отчет за прошлый месяц','COMPLETED','2025-05-30 16:08:41.837280','2025-05-30 16:10:11.625158','2025-05-31 07:00:00.000000',15,11,NULL,'HIGH'),(23,'Проверить чип','Оплатить приглашение на склад 🇨🇳','NEW','2025-05-30 20:13:57.160068','2025-05-30 20:13:57.160085','2025-06-02 15:12:00.000000',16,11,25,'HIGH'),(24,'Тест','Проверка','COMPLETED','2025-05-30 20:18:43.420145','2025-05-30 20:18:59.870763','2025-05-31 07:00:00.000000',15,1,NULL,'HIGH'),(25,'Чек лист','Разработать чек лист по подготовке фуры к рейсу','NEW','2025-06-15 18:31:47.019785','2025-06-15 18:31:47.019808','2025-06-16 07:00:00.000000',16,11,NULL,'HIGH');
/*!40000 ALTER TABLE `logistics_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logistics_vehicle`
--

DROP TABLE IF EXISTS `logistics_vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistics_vehicle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `brand` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `year` int NOT NULL,
  `driver_id` bigint DEFAULT NULL,
  `status` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `vehicle_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `is_archived` tinyint(1) NOT NULL DEFAULT '0',
  `vin_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `engine_number` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `chassis_number` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `engine_capacity` decimal(4,1) DEFAULT NULL,
  `fuel_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fuel_consumption` decimal(4,1) DEFAULT NULL,
  `length` decimal(6,2) DEFAULT NULL,
  `width` decimal(5,2) DEFAULT NULL,
  `height` decimal(5,2) DEFAULT NULL,
  `max_weight` decimal(8,2) DEFAULT NULL,
  `cargo_capacity` decimal(8,2) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `logistics_vehicle_driver_id_6c4cb04e_fk_accounts_user_id` (`driver_id`),
  KEY `logistics_vehicle_created_by_id_fk` (`created_by_id`),
  CONSTRAINT `logistics_vehicle_created_by_id_fk` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `logistics_vehicle_driver_id_6c4cb04e_fk_accounts_user_id` FOREIGN KEY (`driver_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistics_vehicle`
--

LOCK TABLES `logistics_vehicle` WRITE;
/*!40000 ALTER TABLE `logistics_vehicle` DISABLE KEYS */;
INSERT INTO `logistics_vehicle` VALUES (25,'533 ATL 01','Mercedes','Actros 420',2020,NULL,'ACTIVE','TRUCK','','Тандем, голова 70 м3',0,'','','',NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'2025-05-30 12:17:58.404968','2025-05-30 12:17:58.404997',1),(26,'290 ATL 01','DAF','106 480',2021,NULL,'INACTIVE','TRUCK','','Тандем, голова 65 м3',0,'','','',NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'2025-05-30 12:20:23.695493','2025-05-30 12:21:56.294991',1),(29,'484 ATL 01','VOLVO','FH 460',2020,NULL,'ACTIVE','TRUCK','','Тандем, голова 65 м3',0,'','','',NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,'2025-05-30 12:28:28.718264','2025-05-30 12:28:28.718310',1);
/*!40000 ALTER TABLE `logistics_vehicle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logistics_vehicledocument`
--

DROP TABLE IF EXISTS `logistics_vehicledocument`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistics_vehicledocument` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `document_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `number` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `issue_date` date NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `issuing_authority` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `file` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `vehicle_id` bigint NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `logistics_vehicledocument_vehicle_id_idx` (`vehicle_id`),
  KEY `logistics_vehicledocument_created_by_id_idx` (`created_by_id`),
  CONSTRAINT `logistics_vehicledocument_created_by_id_fk` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `logistics_vehicledocument_vehicle_id_fk` FOREIGN KEY (`vehicle_id`) REFERENCES `logistics_vehicle` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistics_vehicledocument`
--

LOCK TABLES `logistics_vehicledocument` WRITE;
/*!40000 ALTER TABLE `logistics_vehicledocument` DISABLE KEYS */;
INSERT INTO `logistics_vehicledocument` VALUES (17,'INSURANCE',NULL,'2025-05-30','2025-07-25',NULL,NULL,'vehicles/25/documents/None_20250530121758.pdf','2025-05-30 12:17:58.452204','2025-05-30 12:17:58.452232',25,1);
/*!40000 ALTER TABLE `logistics_vehicledocument` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logistics_vehiclemaintenance`
--

DROP TABLE IF EXISTS `logistics_vehiclemaintenance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistics_vehiclemaintenance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `maintenance_type` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `mileage` int DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `cost` decimal(10,2) DEFAULT NULL,
  `next_maintenance_date` date DEFAULT NULL,
  `next_maintenance_mileage` int DEFAULT NULL,
  `performed_by` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `vehicle_id` bigint NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `logistics_vehiclemaintenance_vehicle_id_idx` (`vehicle_id`),
  KEY `logistics_vehiclemaintenance_created_by_id_idx` (`created_by_id`),
  CONSTRAINT `logistics_vehiclemaintenance_created_by_id_fk` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `logistics_vehiclemaintenance_vehicle_id_fk` FOREIGN KEY (`vehicle_id`) REFERENCES `logistics_vehicle` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistics_vehiclemaintenance`
--

LOCK TABLES `logistics_vehiclemaintenance` WRITE;
/*!40000 ALTER TABLE `logistics_vehiclemaintenance` DISABLE KEYS */;
/*!40000 ALTER TABLE `logistics_vehiclemaintenance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logistics_vehiclephoto`
--

DROP TABLE IF EXISTS `logistics_vehiclephoto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistics_vehiclephoto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `photo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_main` tinyint(1) NOT NULL DEFAULT '0',
  `uploaded_at` datetime(6) NOT NULL,
  `vehicle_id` bigint NOT NULL,
  `uploaded_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `logistics_vehiclephoto_vehicle_id_idx` (`vehicle_id`),
  KEY `logistics_vehiclephoto_uploaded_by_id_idx` (`uploaded_by_id`),
  CONSTRAINT `logistics_vehiclephoto_uploaded_by_id_fk` FOREIGN KEY (`uploaded_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `logistics_vehiclephoto_vehicle_id_fk` FOREIGN KEY (`vehicle_id`) REFERENCES `logistics_vehicle` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistics_vehiclephoto`
--

LOCK TABLES `logistics_vehiclephoto` WRITE;
/*!40000 ALTER TABLE `logistics_vehiclephoto` DISABLE KEYS */;
INSERT INTO `logistics_vehiclephoto` VALUES (8,'vehicles/new/photos/photo_20250530121758.png',NULL,1,'2025-05-30 12:17:58.416417',25,1),(9,'vehicles/new/photos/photo_20250530121758.jpg',NULL,0,'2025-05-30 12:17:58.427861',25,1),(10,'vehicles/new/photos/photo_20250530121758.jpeg',NULL,0,'2025-05-30 12:17:58.436860',25,1),(11,'vehicles/new/photos/photo_20250530121758_JsBbCdX.jpeg',NULL,0,'2025-05-30 12:17:58.444330',25,1),(12,'vehicles/new/photos/photo_20250530122023.png',NULL,1,'2025-05-30 12:20:23.710774',26,1),(13,'vehicles/new/photos/photo_20250530122023.webp',NULL,0,'2025-05-30 12:20:23.719616',26,1),(14,'vehicles/new/photos/photo_20250530122023.jpeg',NULL,0,'2025-05-30 12:20:23.729772',26,1),(20,'vehicles/new/photos/photo_20250530122828.png',NULL,1,'2025-05-30 12:28:28.731711',29,1),(21,'vehicles/new/photos/photo_20250530122828.jpg',NULL,0,'2025-05-30 12:28:28.757556',29,1),(22,'vehicles/new/photos/photo_20250530122828.jpeg',NULL,0,'2025-05-30 12:28:28.767751',29,1),(23,'vehicles/new/photos/photo_20250530122828_DcMcj87.jpeg',NULL,0,'2025-05-30 12:28:28.780792',29,1),(24,'vehicles/new/photos/photo_20250530122828_NORqRDx.jpeg',NULL,0,'2025-05-30 12:28:28.793624',29,1);
/*!40000 ALTER TABLE `logistics_vehiclephoto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logistics_waybilldocument`
--

DROP TABLE IF EXISTS `logistics_waybilldocument`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistics_waybilldocument` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `departure_point` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `destination_point` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cargo_description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `cargo_weight` decimal(10,2) NOT NULL,
  `created_by_id` bigint NOT NULL,
  `driver_id` bigint NOT NULL,
  `vehicle_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number` (`number`),
  KEY `logistics_waybilldoc_created_by_id_133a371c_fk_accounts_` (`created_by_id`),
  KEY `logistics_waybilldocument_driver_id_549880e1_fk_accounts_user_id` (`driver_id`),
  KEY `logistics_waybilldoc_vehicle_id_acd255e7_fk_logistics` (`vehicle_id`),
  CONSTRAINT `logistics_waybilldoc_created_by_id_133a371c_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `logistics_waybilldoc_vehicle_id_acd255e7_fk_logistics` FOREIGN KEY (`vehicle_id`) REFERENCES `logistics_vehicle` (`id`),
  CONSTRAINT `logistics_waybilldocument_driver_id_549880e1_fk_accounts_user_id` FOREIGN KEY (`driver_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistics_waybilldocument`
--

LOCK TABLES `logistics_waybilldocument` WRITE;
/*!40000 ALTER TABLE `logistics_waybilldocument` DISABLE KEYS */;
/*!40000 ALTER TABLE `logistics_waybilldocument` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-20 11:56:39

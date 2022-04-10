-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server Version:               10.3.29-MariaDB-0+deb10u1 - Raspbian 10
-- Server Betriebssystem:        debian-linux-gnueabihf
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Exportiere Datenbank Struktur für dlc
DROP DATABASE IF EXISTS `dlc`;
CREATE DATABASE IF NOT EXISTS `dlc` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `dlc`;

-- Exportiere Struktur von Tabelle dlc.driving_licenses
DROP TABLE IF EXISTS `driving_licenses`;
CREATE TABLE IF NOT EXISTS `driving_licenses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL,
  `staff_id` int(11) NOT NULL,
  `license_nr` varchar(50) NOT NULL,
  `rfid` varchar(50) NOT NULL,
  `check_interval` int(11) NOT NULL DEFAULT 0,
  `authority` text NOT NULL DEFAULT '',
  `date_issue` date DEFAULT NULL,
  `date_valid` date DEFAULT NULL,
  `enlisted` tinyint(4) NOT NULL DEFAULT 0,
  `last_user_id` int(11) DEFAULT 0,
  `last_access` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`uuid`) USING BTREE,
  UNIQUE KEY `rfid` (`rfid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COMMENT='Driving Licenses\r\nFührerscheine';

-- Exportiere Daten aus Tabelle dlc.driving_licenses: ~0 rows (ungefähr)
/*!40000 ALTER TABLE `driving_licenses` DISABLE KEYS */;
INSERT INTO `driving_licenses` (`id`, `uuid`, `staff_id`, `license_nr`, `rfid`, `check_interval`, `authority`, `date_issue`, `date_valid`, `enlisted`, `last_user_id`, `last_access`) VALUES
	(3, '9ba4008c-3312-11ec-a134-0d0802f3bbd0', 1, 'TEST_license_nr', 'TEST_rfid', 0, 'TEST_authority', '2021-10-22', '2021-10-22', 0, 0, '2021-10-22 18:08:06'),
	(4, '1d94883b-33b0-11ec-a134-0d0802f3bbd0', 6, 'GammeltKørekort', 'UlleBulle', 28, 'Kamelloohsa', NULL, NULL, 0, 0, '2021-10-23 07:00:23');
/*!40000 ALTER TABLE `driving_licenses` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle dlc.driving_licenses_control
DROP TABLE IF EXISTS `driving_licenses_control`;
CREATE TABLE IF NOT EXISTS `driving_licenses_control` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL,
  `rfid` varchar(50) NOT NULL,
  `control_time` datetime NOT NULL,
  `staff_id` int(11) NOT NULL DEFAULT 0,
  `remarks` text NOT NULL DEFAULT '',
  `device_id` text NOT NULL DEFAULT '',
  `last_user_id` int(11) DEFAULT NULL,
  `last_access` datetime DEFAULT NULL,
  `fetched` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`,`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COMMENT='Driving Licenses Control\r\nFührerscheinkontrollen';

-- Exportiere Daten aus Tabelle dlc.driving_licenses_control: ~1 rows (ungefähr)
/*!40000 ALTER TABLE `driving_licenses_control` DISABLE KEYS */;
INSERT INTO `driving_licenses_control` (`id`, `uuid`, `rfid`, `control_time`, `staff_id`, `remarks`, `device_id`, `last_user_id`, `last_access`, `fetched`) VALUES
	(23, '244ebb17-3355-11ec-bddd-901b0ed52fc1', 'TEST_rfid', '2021-10-22 00:00:00', 1, '', 'TEST_sp', NULL, '2021-10-22 18:28:58', 0);
/*!40000 ALTER TABLE `driving_licenses_control` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle dlc.due_dates_staff
DROP TABLE IF EXISTS `due_dates_staff`;
CREATE TABLE IF NOT EXISTS `due_dates_staff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL,
  `staff_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `last_user_id` int(11) DEFAULT NULL,
  `last_access` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`uuid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Due Dates Staff\r\nFälligkeiten Personal';

-- Exportiere Daten aus Tabelle dlc.due_dates_staff: ~0 rows (ungefähr)
/*!40000 ALTER TABLE `due_dates_staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `due_dates_staff` ENABLE KEYS */;

-- Exportiere Struktur von Tabelle dlc.due_date_types
DROP TABLE IF EXISTS `due_date_types`;
CREATE TABLE IF NOT EXISTS `due_date_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL,
  `type` varchar(50) NOT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `last_user_id` int(11) DEFAULT NULL,
  `last_access` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`uuid`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Due Date Types\r\nFälligkeitsarten';

-- Exportiere Daten aus Tabelle dlc.due_date_types: ~0 rows (ungefähr)
/*!40000 ALTER TABLE `due_date_types` DISABLE KEYS */;
/*!40000 ALTER TABLE `due_date_types` ENABLE KEYS */;

-- Exportiere Struktur von Prozedur dlc.sp_insert_driving_licenses_checks
DROP PROCEDURE IF EXISTS `sp_insert_driving_licenses_checks`;
DELIMITER //
CREATE PROCEDURE `sp_insert_driving_licenses_checks`(
	IN `date_creation` DATETIME,
	IN `rfid_in` VARCHAR(50),
	IN `deviceid_in` VARCHAR(50),
	OUT `driver_id` INT,
	OUT `driver_lastname` VARCHAR(50),
	OUT `driver_firstname` VARCHAR(50),
	OUT `driver_interval` INT,
	OUT `ret` TINYINT
)
    COMMENT 'Insert Driving Licenses Check - equiv. SQL Server'
BEGIN
	SET driver_id = 0;
	SET driver_lastname = "";
	SET driver_firstname = "";
	SET driver_interval = 0;
	SET ret = 0;
	SELECT staff_id INTO driver_id FROM driving_licenses WHERE rfid = rfid_in;
	IF driver_id > 0 THEN
		INSERT INTO driving_licenses_control (rfid, control_time, staff_id, device_id)
 		VALUES (rfid_in, date_creation, driver_id, deviceid_in);
 		SELECT last_name INTO driver_lastname FROM staff WHERE id = driver_id;
		SELECT first_name INTO driver_firstname FROM staff WHERE id = driver_id;
		SELECT check_interval INTO driver_interval FROM driving_licenses WHERE rfid = rfid_in;
 		SET ret = 1;
 	END IF;
END//
DELIMITER ;

-- Exportiere Struktur von Tabelle dlc.staff
DROP TABLE IF EXISTS `staff`;
CREATE TABLE IF NOT EXISTS `staff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL,
  `last_name` text NOT NULL DEFAULT '',
  `first_name` text NOT NULL DEFAULT '',
  `address` text NOT NULL DEFAULT '',
  `zip_code` text NOT NULL DEFAULT '',
  `city` text NOT NULL DEFAULT '',
  `country` text NOT NULL DEFAULT '',
  `email` text NOT NULL DEFAULT '',
  `phone` text NOT NULL DEFAULT '',
  `user` tinyint(4) DEFAULT 0,
  `last_user_id` int(11) DEFAULT NULL,
  `last_access` datetime DEFAULT NULL,
  PRIMARY KEY (`id`,`uuid`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COMMENT='Staff\r\nPersonal';

-- Exportiere Daten aus Tabelle dlc.staff: ~3 rows (ungefähr)
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` (`id`, `uuid`, `last_name`, `first_name`, `address`, `zip_code`, `city`, `country`, `email`, `phone`, `user`, `last_user_id`, `last_access`) VALUES
	(1, '667a09ab-3095-11ec-ad51-2fa093035399', 'Mustermann', 'Max', 'Hauptstraße 1', '72505', 'Göggingen', 'Germany', 'mustermann@domain.tld', '+49 1234 567890', 0, NULL, '2021-10-22 18:05:50'),
	(6, '8cfc7378-3344-11ec-a134-0d0802f3bbd0', 'Harzmann', 'Jörg', 'Birkestræde 47', '5150', 'Rudkøbing', 'Denmark', 'harzmann@domain.tld', '+42 555 112233', 0, NULL, '2021-10-23 06:51:43');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;

-- Exportiere Struktur von Trigger dlc.driving_licenses_before_insert
DROP TRIGGER IF EXISTS `driving_licenses_before_insert`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `driving_licenses_before_insert` BEFORE INSERT ON `driving_licenses` FOR EACH ROW BEGIN
	SET NEW.uuid=UUID();
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger dlc.driving_licenses_before_update
DROP TRIGGER IF EXISTS `driving_licenses_before_update`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `driving_licenses_before_update` BEFORE UPDATE ON `driving_licenses` FOR EACH ROW BEGIN
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger dlc.driving_licenses_control_before_insert
DROP TRIGGER IF EXISTS `driving_licenses_control_before_insert`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `driving_licenses_control_before_insert` BEFORE INSERT ON `driving_licenses_control` FOR EACH ROW BEGIN
	SET NEW.uuid=UUID();
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger dlc.driving_licenses_control_before_update
DROP TRIGGER IF EXISTS `driving_licenses_control_before_update`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `driving_licenses_control_before_update` BEFORE UPDATE ON `driving_licenses_control` FOR EACH ROW BEGIN
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger dlc.due_dates_staff_before_insert
DROP TRIGGER IF EXISTS `due_dates_staff_before_insert`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `due_dates_staff_before_insert` BEFORE INSERT ON `due_dates_staff` FOR EACH ROW BEGIN
	SET NEW.uuid=UUID();
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger dlc.due_dates_staff_before_update
DROP TRIGGER IF EXISTS `due_dates_staff_before_update`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `due_dates_staff_before_update` BEFORE UPDATE ON `due_dates_staff` FOR EACH ROW BEGIN
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger dlc.due_date_types_before_insert
DROP TRIGGER IF EXISTS `due_date_types_before_insert`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `due_date_types_before_insert` BEFORE INSERT ON `due_date_types` FOR EACH ROW BEGIN
	SET NEW.uuid=UUID();
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger dlc.due_date_types_before_update
DROP TRIGGER IF EXISTS `due_date_types_before_update`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `due_date_types_before_update` BEFORE UPDATE ON `due_date_types` FOR EACH ROW BEGIN
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger dlc.staff_before_insert
DROP TRIGGER IF EXISTS `staff_before_insert`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `staff_before_insert` BEFORE INSERT ON `staff` FOR EACH ROW BEGIN
	SET NEW.uuid=UUID();
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Exportiere Struktur von Trigger dlc.staff_before_update
DROP TRIGGER IF EXISTS `staff_before_update`;
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `staff_before_update` BEFORE UPDATE ON `staff` FOR EACH ROW BEGIN
	SET NEW.last_access=NOW();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

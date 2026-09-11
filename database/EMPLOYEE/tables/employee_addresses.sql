CREATE TABLE `employee_addresses` (
  `address_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `address_line1` varchar(200) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT 'India',
  `postal_code` varchar(20) DEFAULT NULL,
  `address_type` enum('Home','Office') DEFAULT 'Home',
  PRIMARY KEY (`address_id`),
  KEY `fk_address_employee` (`employee_id`),
  CONSTRAINT `fk_address_employee` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

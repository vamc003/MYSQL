CREATE TABLE `employee_projects` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `project_name` varchar(150) NOT NULL,
  `project_role` varchar(100) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `project_status` enum('Planned','Active','Completed') DEFAULT 'Active',
  PRIMARY KEY (`project_id`),
  KEY `idx_project_employee` (`employee_id`),
  CONSTRAINT `fk_project_employee` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

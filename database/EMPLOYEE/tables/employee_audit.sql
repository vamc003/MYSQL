CREATE TABLE `employee_audit` (
  `audit_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int DEFAULT NULL,
  `action_type` varchar(50) DEFAULT NULL,
  `action_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`audit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

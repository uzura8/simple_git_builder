CREATE TABLE `transaction_preset` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) NOT NULL,
  `transaction_name` varchar(512) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `account_code` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `account_code` (`account_code`),
  CONSTRAINT `transaction_preset_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `transaction_preset_ibfk_2` FOREIGN KEY (`account_code`) REFERENCES `account` (`code`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

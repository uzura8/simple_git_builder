CREATE TABLE `contact` (
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `code` varchar(6) NOT NULL,
  `subject` varchar(64) NOT NULL,
  `content` text NOT NULL,
  `email` varchar(128) NOT NULL,
  `tel` varchar(12) DEFAULT NULL,
  `name` varchar(248) DEFAULT NULL,
  `name_phonetic` varchar(248) DEFAULT NULL,
  `contact_type` tinyint(4) DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

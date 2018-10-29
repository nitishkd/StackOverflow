create DATABASE stackoverflow;

use stackoverflow;

CREATE TABLE `stackoverflow`.`users` (
  `userid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `alias` VARCHAR(255) NOT NULL,
  `useremail` VARCHAR(255) NOT NULL,
  `userpass` VARCHAR(255) NOT NULL,
  `userrating` INT UNSIGNED NULL,
  PRIMARY KEY (`userid`),
  UNIQUE INDEX `alias_UNIQUE` (`alias` ASC),
  UNIQUE INDEX `useremail_UNIQUE` (`useremail` ASC)
  );





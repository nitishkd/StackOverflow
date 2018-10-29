create DATABASE stackoverflow;

use stackoverflow;

CREATE TABLE `stackoverflow`.`users` (
  `userid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `alias` VARCHAR(255) NOT NULL,
  `useremail` VARCHAR(255) NOT NULL,
  `userpass` VARCHAR(255) NOT NULL,
  `userrating` INT UNSIGNED NULL,
  `datetime` DATETIME NULL,
  PRIMARY KEY (`userid`),
  UNIQUE INDEX `alias_UNIQUE` (`alias` ASC),
  UNIQUE INDEX `useremail_UNIQUE` (`useremail` ASC)
  );

CREATE TABLE `stackoverflow`.`questions` (
  `qid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `heading` VARCHAR(255) NOT NULL,
  `body` VARCHAR(5000) NOT NULL,
  `upvotes` INT NULL DEFAULT 0,
  `userid` INT UNSIGNED NULL,
  `datetime` DATETIME NULL,
  `bestAnswer` INT NULL DEFAULT -1,
  PRIMARY KEY (`qid`))
  ;

CREATE TABLE `stackoverflow`.`answers` (
  `ansid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `qid` INT UNSIGNED NULL,
  `body` VARCHAR(10000) NULL,
  `upvotes` INT NULL DEFAULT 0,
  `userid` INT UNSIGNED NOT NULL,
  `datetime` DATETIME NULL,
  PRIMARY KEY (`ansid`)
  );

CREATE TABLE `stackoverflow`.`qncomment` (
  `commentid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `body` VARCHAR(255) NULL,
  `userid` INT UNSIGNED NOT NULL,
  `qid` INT UNSIGNED NOT NULL,
  `datetime` DATETIME NULL,
  PRIMARY KEY (`commentid`)
  );

CREATE TABLE `stackoverflow`.`anscomment` (
  `commentid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `body` VARCHAR(255) NULL,
  `userid` INT UNSIGNED NOT NULL,
  `ansid` INT UNSIGNED NOT NULL,
  `datetime` DATETIME NULL,
  PRIMARY KEY (`commentid`)
  );

CREATE TABLE `stackoverflow`.`tags` (
  `tagid` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `userid` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`tagid`));

CREATE TABLE `stackoverflow`.`qnTags` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tagid` INT UNSIGNED NOT NULL,
  `qid` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`));





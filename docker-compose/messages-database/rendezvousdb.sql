-- MySQL Script generated by MySQL Workbench
-- lun 3 mag 2021, 16:13:46
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema rendezvous-chatroom
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `rendezvous-chatroom` ;
USE `rendezvous-chatroom` ;

-- -----------------------------------------------------
-- Table `rendezvous-chatroom`.`message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rendezvous-chatroom`.`message` (
  `sender_name` VARCHAR(32) NOT NULL,
  `content` VARCHAR(600) NOT NULL,
  `server_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `id` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

DELIMITER $$

DROP PROCEDURE IF EXISTS `add_user`$$

CREATE PROCEDURE `add_user`(IN `p_Name` VARCHAR(45), IN `p_Passw` VARCHAR(200))
BEGIN
    DECLARE `_HOST` CHAR(14) DEFAULT '@\'%\'';
    DECLARE `_DB_NAME` VARCHAR(50) default CONCAT(p_Name, '_db');
    SET `p_Name` := CONCAT('\'', REPLACE(TRIM(`p_Name`), CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\''),
    `p_Passw` := CONCAT('\'', REPLACE(`p_Passw`, CHAR(39), CONCAT(CHAR(92), CHAR(39))), '\'');

    SET @`sql` := CONCAT('CREATE USER ', `p_Name`, `_HOST`, ' IDENTIFIED BY ', `p_Passw`);
    PREPARE `stmt` FROM @`sql`;
    EXECUTE `stmt`;

    SET @`sql` := CONCAT('CREATE DATABASE ', `_DB_NAME`);
    PREPARE `stmt` FROM @`sql`;
    EXECUTE `stmt`;

    SET @`sql` := CONCAT('GRANT ALL PRIVILEGES ON ', _DB_NAME, '.* TO ', `p_Name`, `_HOST`);
    PREPARE `stmt` FROM @`sql`;
    EXECUTE `stmt`;

    DEALLOCATE PREPARE `stmt`;
    FLUSH PRIVILEGES;
END$$

DELIMITER ;
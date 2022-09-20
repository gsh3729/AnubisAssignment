DROP DATABASE IF EXISTS filesdb;
CREATE DATABASE filesdb;
USE filesdb;
DROP TABLE IF EXISTS file_table;

CREATE TABLE if not exists file_table (
    id int NOT NULL AUTO_INCREMENT,
    filename varchar(255) NOT NULL,
    file MEDIUMBLOB,
    PRIMARY KEY (id)
);
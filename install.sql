GRANT ALL PRIVILEGES ON *.* TO 'project3'@'localhost' IDENTIFIED BY 'project3';

update mysql.user set plugin = 'mysql_native_password' where User='test';

FLUSH PRIVILEGES;




 CREATE DATABASE project3;

 use project3;

CREATE TABLE users (id INT(10)  AUTO_INCREMENT PRIMARY KEY  , name  VARCHAR(100), email VARCHAR(100),  username VARCHAR(100), password VARCHAR(100));



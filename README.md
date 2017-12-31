# Pyduplicateimagechecker
Imports images from dir to mysql db with md5, filename, path, size, timestamps then does a duplicate check against existing files in the dir
Also can rebuild from the database to copy files with exif jpeg folder structure by year/month_day_md5.jpg etc..

  - insertfilesdatabase.py - imports directory structure into database with md5 and more
  - rebuildimages.py - pulls files from SQL to copy to new structure, skipping duplicate files found
  - 
# insertfilesdatabase.py 

 - database structure 
  ```
  CREATE TABLE pictures (
  id int(11) unsigned NOT NULL AUTO_INCREMENT,
  filename varchar(300) DEFAULT NULL,
  filepath varchar(2000) DEFAULT NULL,
  size bigint(255) unsigned DEFAULT NULL,
  md5 varchar(1000) DEFAULT NULL,
  datetimedigitized varchar(30) DEFAULT NULL,
  datetimeoriginal varchar(30) DEFAULT NULL,
  filetimestamp varchar(30) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=31784 DEFAULT CHARSET=utf8mb4;
```
  
  - there are a lot of required python libraries I did not list them all here
  ```
  # pip install mysqlclient
# sudo add-apt-repository ppa:deadsnakes/ppa
# sudo apt-get update
# sudo apt-get install python3.6
  ```



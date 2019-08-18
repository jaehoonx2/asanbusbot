# asanbusbot
* A Python-based telegram bot that serves bus information of Asan city, Korea
* Asan Bus Information System Homepage : http://bus.asan.go.kr/web/main

# Getting Started
* Python 3.6 or upper version is needed.
* python-telegram-bot, requests and pymysql should be installed.
* MariaDB@10.3 is also used and SQL queries that used in the project are as below.

# etc.
* Install modules (pip - Win, pip3 - MacOS or Linux)
    - pip/pip3 install python-telegram-bot
    - pip/pip3 install requests
    - pip/pip3 install pymysql

* MariaDB query
```
CREATE TABLE stops (                            # Table 'stops' from DBHelper.py
	name VARCHAR(50) NOT NULL PRIMARY KEY,
	id1 VARCHAR(50) NOT NULL,
	id2 VARCHAR(50) NULL DEFAULT NULL
	) ENGINE = InnoDB;
```
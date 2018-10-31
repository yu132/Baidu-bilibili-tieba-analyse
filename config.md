## 安装mysqlb并配置远程连接
```
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev

sudo ufw allow 3306
mysql -uroot -p
use mysql;
select host,user from user where user='root';
update user set host='%' where user='root';

sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
将bind-address = 127.0.0.1注释掉（即在行首加#）

service mysql restart
```

### 修改mysql编码至utf8mb4
```
sudo gedit /etc/mysql/my.cnf

加上下面这段
[client] 
default-character-set = utf8mb4

[mysql] 
default-character-set = utf8mb4

[mysqld] 
character-set-client-handshake = FALSE 
character-set-server = utf8mb4 
collation-server = utf8mb4_unicode_ci 
init_connect=’SET NAMES utf8mb4’

service mysql restart
```


## 安装python3
### python3:
```
sudo apt-get install python3-pip
sudo cp /usr/bin/python /usr/bin/python_bak
sudo rm /usr/bin/python
sudo ln -s /usr/bin/python3.5 /usr/bin/python
```
### pip3:
```
sudo apt-get install python3-pip
pip3 install --upgrade pip
```
### import:
```
pip3 install scrapy
pip3 install pymysql
pip3 install configparser
pip3 install DBUtils
```
### scrapy:
```
sudo apt install python-scrapy
```

### 运行
```
scrapy crawl baidu_spider
```

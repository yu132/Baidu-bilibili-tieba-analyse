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

service mysql restart<br>
```
## 安装python3
### python3:
```
sudo apt-get install python3-pip<br>
sudo cp /usr/bin/python /usr/bin/python_bak<br>
sudo rm /usr/bin/python<br>
sudo ln -s /usr/bin/python3.5 /usr/bin/python<br>
```
### pip3:
```
sudo apt-get install python3-pip<br>
```
### import:
```
pip3 install scrapy<br>
pip3 install pymysql<br>
pip3 install configparser<br>
pip3 install DBUtils<br>
```

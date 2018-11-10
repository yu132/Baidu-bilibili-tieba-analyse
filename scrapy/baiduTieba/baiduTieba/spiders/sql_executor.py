# -*- coding: utf-8 -*-
from DBUtils.PooledDB import PooledDB

import pymysql
import configparser

main_page_ddl="""CREATE TABLE IF NOT EXISTS `main_page_info` (
   `mp_id` int(11) NOT NULL AUTO_INCREMENT,
   `time` bigint(20) NOT NULL,
   `max_page` int(11) NOT NULL,
   PRIMARY KEY (`mp_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

tiezi_scan_ddl="""CREATE TABLE IF NOT EXISTS `tiezi_scan` (
   `ts_id` int(11) NOT NULL AUTO_INCREMENT,
   `start_time` bigint(20) NOT NULL,
   `next_start_index` bigint(20) NOT NULL,
   PRIMARY KEY (`ts_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

tiezi_ddl="""CREATE TABLE IF NOT EXISTS `tiezi_info` (
   `tz_id` int(11) NOT NULL AUTO_INCREMENT,
   `tid` bigint(20) NOT NULL,
   `mp_id` int(11) NOT NULL,
   `ts_id` int(11) DEFAULT NULL,
   PRIMARY KEY (`tz_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

base_tiezi_info_ddl="""CREATE TABLE IF NOT EXISTS `base_tiezi_info` (
   `tid` bigint(20) NOT NULL,
   `reply_num` int(11) NOT NULL,
   `link` varchar(255) NOT NULL,
   `title` varchar(255) NOT NULL,
   `author_name` varchar(100) DEFAULT NULL,
   `author_home_page_link` varchar(255) DEFAULT NULL,
   `summary` text,
   `replier_name` varchar(255) DEFAULT NULL,
   `replier_home_page_link` varchar(255) DEFAULT NULL,
   PRIMARY KEY (`tid`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

tiezi_content_info_ddl="""CREATE TABLE IF NOT EXISTS `tiezi_content_info` (
   `content_id` bigint(20) NOT NULL AUTO_INCREMENT,
   `pid` bigint(20) DEFAULT NULL,
   `tid` bigint(20) DEFAULT NULL,
   `author_name` varchar(100) DEFAULT NULL,
   `author_level` int(3) DEFAULT NULL,
   `author_home_page_link` varchar(255) DEFAULT NULL,
   `content` text,
   `floor` int(11) DEFAULT NULL,
   `time` varchar(20) DEFAULT NULL,
   `client_type` varchar(20) DEFAULT NULL,
   PRIMARY KEY (`content_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

louzhonglou_info_ddl="""CREATE TABLE IF NOT EXISTS `louzhonglou_info` (
   `louzhonglou_id` bigint(20) NOT NULL AUTO_INCREMENT,
   `tid` bigint(20) DEFAULT NULL,
   `pid` bigint(20) DEFAULT NULL,
   `author_name` varchar(100) DEFAULT NULL,
   `content` text,
   `time` varchar(30) DEFAULT NULL,
   PRIMARY KEY (`louzhonglou_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

image_info_ddl="""CREATE TABLE IF NOT EXISTS `image_info` (
   `image_id` bigint(20) NOT NULL AUTO_INCREMENT,
   `src` varchar(255) DEFAULT NULL,
   `tid` bigint(20) DEFAULT NULL,
   `pid` bigint(20) DEFAULT NULL,
   `tiezi_content_id` bigint(20) DEFAULT NULL,
   PRIMARY KEY (`image_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

emoji_info_ddl="""CREATE TABLE IF NOT EXISTS `emoji_info` (
   `emoji_id` bigint(20) NOT NULL AUTO_INCREMENT,
   `src` varchar(255) DEFAULT NULL,
   `word` varchar(30) DEFAULT NULL,
   PRIMARY KEY (`emoji_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

emoji_louzhonglou_relationship_ddl=\
"""CREATE TABLE IF NOT EXISTS `emoji_louzhonglou_relationship` (
   `emoji_louzhonglou_relationship_id` bigint(20) NOT NULL AUTO_INCREMENT,
   `louzhonglou_id` bigint(20) DEFAULT NULL,
   `emoji_id` bigint(20) DEFAULT NULL,
   PRIMARY KEY (`emoji_louzhonglou_relationship_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""

emoji_tiezi_content_relationship_ddl=\
"""CREATE TABLE IF NOT EXISTS `emoji_tiezi_content_relationship` (
   `emoji_tiezi_content_relationship_id` bigint(20) NOT NULL AUTO_INCREMENT,
   `tiezi_content_info_id` bigint(20) DEFAULT NULL,
   `emoji_id` bigint(20) DEFAULT NULL,
   PRIMARY KEY (`emoji_tiezi_content_relationship_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""


def get_db_pool():
    mysql_conf_file="mysql.config"

    config=configparser.ConfigParser()

    config.read(mysql_conf_file)

    try:
        host=config.get("db","host")
    except:
        host="localhost"
        
    try:
        username=config.get("db","username")
    except:
        print("database username not exists")
        raise RuntimeError('db config error')

    try:
        password=config.get("db","password")
    except:
        print("database password not exists")
        raise RuntimeError('db config error')

    try:
        dbName=config.get("db","db")
    except:
        dbName="tieba_spider"
        

    print(host)
    print(dbName)

    pool = PooledDB(pymysql,5,host=host,user=username,passwd=password,db=dbName,port=3306,charset="utf8") #5为连接池里的最少连接数

    return pool

pool=get_db_pool()

def excute_sql(cursor,sql,args=None):
    if args:
        cursor.execute(sql,args)
    else:
        cursor.execute(sql)

def query(sql,args=None):
    conn = pool.connection()
    cursor=conn.cursor()
    
    excute_sql(cursor,sql,args)

    data = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return data

def execute_update(sql,args=None):
    conn = pool.connection()
    cursor=conn.cursor()

    excute_sql(cursor,sql,args)

    conn.commit()
    
    cursor.close()
    conn.close()

def execute(sql,args=None):
    conn = pool.connection()
    cursor=conn.cursor()
    
    excute_sql(cursor,sql,args)
    
    cursor.close()
    conn.close()

def insert_and_get_id(sql,args=None):
    conn = pool.connection()
    cursor=conn.cursor()

    excute_sql(cursor,sql,args)

    id_=int(cursor.lastrowid)

    conn.commit()
    
    cursor.close()
    conn.close()

    return id_

execute(main_page_ddl)
execute(tiezi_scan_ddl)
execute(tiezi_ddl)
execute(base_tiezi_info_ddl)

execute(tiezi_content_info_ddl)
execute(louzhonglou_info_ddl)
execute(image_info_ddl)
execute(emoji_info_ddl)
execute(emoji_louzhonglou_relationship_ddl)
execute(emoji_tiezi_content_relationship_ddl)

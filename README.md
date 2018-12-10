# Baidu-bilibili-tieba-analyse
对百度bilibil吧主题帖进行分析

## 分析原因
由于本人日常刷bilibili吧，又由于本人有课题需要提交，所以选取了这个题目进行分析。

## 分析价值
bilibili吧作为一个讨论acg的贴吧，由于吧务管理较为严格，所以产出的帖子较其余贴吧可能稍微质量高一些，拿来做分析可能还行，而且贴吧的帖子文本量很大，用于做大数据分析非常适合。

## 抓取速率
改进后都是3秒或2秒一爬，速度较慢，可以+IP代理和UserAgent轮转，尚不知道贴吧对访问速率是否有限制。

## 如何抓取百度贴吧内容
请见[teiba.md](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/tieba.md)  

## 工具：
使用的爬虫（scrapy实现的）：
https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/scrapy

查询用sql：
[sqls.txt](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/sqls.txt)  

## 结果展示
词云（只使用全部题目来做的）：
![b吧娘](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/result/pic2.jpg) 

发帖用户等级分布：
![](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/result/bar.jpg) 

帖子随月份的分布：
![](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/result/bar2.jpg) 

客户端使用占比：
![](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/result/pie_1.jpg) 

发主题贴最多的用户：
请见[author1.md](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/result/author1.md) 

发回复贴最多的用户：
请见[author.md](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/result/author.md)

帖子每小时的分布：
请见[time_hour.md](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/result/time_hour.md)

# Baidu-bilibili-tieba-analyse
对百度bilibil吧主题帖进行分析

## 分析原因
由于本人日常刷bilibili吧，又由于本人有课题需要提交，所以选取了这个题目进行分析

## 分析价值
~~由于百度贴吧对帖子进行了限制，所以最多能够看最近2000页的主题帖（之后发现可以绕过限制，不过不知道可以用多久），一个页面共50个帖子，所以最多能够查看到10,0000个帖子，但是由于访问时各个页面之间会出现重复，加上一些处理上的问题，所以最后剩下的就只有大约9,5000个主题帖，但是数据规模还是很大，足够观察出一些有价值的东西。~~现在发现全部页面都可以抓取，所以需要重新编写部分的爬虫，最终选择重新实现

## 抓取速率
由于尽量不给对应服务器造成压力，所以对于百度的爬取都是单线程+休眠1秒/主页或主题帖，爬取楼中楼的时候是单线程+休眠250ms/页，对于萌娘百科的爬取是单线程+休眠5秒/页，所以进度会比较慢

## 如何抓取百度贴吧内容
请见[teiba.md](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/tieba.md)  

## 进度记录

### bilibili吧数据
+ 2018/10/10-2018/10/11 爬取百度bilibili吧主页（共两千页）+清洗对应数据
+ 2018/10/12-2018/10/16 爬取共计95000余个主题帖的回复信息，不包括楼中楼
+ 2018/10/16-2018/10/19 爬取楼中楼主要信息
+ 2018/10/19-2018/10/21 爬取楼中楼其他信息
+ 2018/10/23-now 重写爬虫，爬取主页信息（目前爬取共86w个主题帖）

### acg词汇数据
+ 2018/10/15 爬取萌娘百科所有词条信息+筛取对应词
+ 2018/10/15-now 爬取百度百科相关词条（爬不动了，可能被ban了）

## 结果展示
词云：
![b吧娘](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/pic2.jpg) 

# 使用须知
1.首先，您需要知道有关mysql的大量知识和scrapy的相关知识，否则很可能会遇到错误<br>
2.其次，本爬虫只在ubuntu16.04系统测试可用，其余系统均未测试，可能会出现不可预料的错误<br>
3.而且，本爬虫只是一个简易的百度贴吧爬虫，并没有考虑过多的意外情况，只能保证基本可运行，并且只适用于当前百度贴吧的页面构造，当页面构造改变的时候，本爬虫也会废弃

# 配置
### 1.配置数据库
(1).首先需要一个mysql数据库，并且需要将数据库编码替换成utfmb4，因为贴吧的名称和内容不可避免的会出现emoji，但是由于mysql的utf8编码并不支持4位的UTF-8编码，因此需要进行修改<br>
(2).您需要在scrapy/baiduTieba/下创建一个名称为mysql.config的文件，并且配置一个格式如下的文件：
```
[db]
username=您的数据库用户名
password=您的数据库密码
db=您的数据库名称
host=您的数据库地址

```
db的默认值为tieba_spider，host默认值为localhost，前面两者可以没有。但是账号和密码均不能为空，否则会出错。
如果以上的配置不能满足您对数据库配置的需求，请自行修改scrapy/baiduTieba/baiduTieba/spiders下的sql_executor中的get_db_pool()方法
### 2.配置爬虫代码
本爬虫有两个部分，第一个部分是爬取贴吧主页的，即有很多个主题帖题目，点进去可以查看帖子详细内容的爬虫，第二个部分是爬取详细内容的爬虫

第一个部分是默认爬取全部的，如果只需要爬取指定数量页面请在baidu_spider.py中的class BaiduTiebaMainPageSpider中修改def parse_first(self,response)中的循环yield返回的数量，提前返回

第二个部分是爬取第一个部分爬回来的帖子编号进行爬取详细内容的。由于数据规模巨大，在baidu_spider_tiezi.py中有STEP_EACH_TIEZI_SCAN参数，您可以配置每一次需要爬取的量，如果磁盘不够，肯定会出错，请注意，本爬虫并没有处理相关的情况的代码。

# 执行（linux下）
请使用scrapy/baiduTieba/下的start.sh和start2.sh启动，这个shell默认会将程序挂到后台，并且以nohup形式执行，退出控制台时也不会关闭程序，输出会重定向到log.file中，如果需要在运行时修改爬虫状态，请使用scrapy的telnet客户端进行对应的操作

# 数据库设计
### 第一部分的表：

main_page_info -> 主页扫描信息 重要性：低<br>
tiezi_info -> 提供一些最重要的主页信息给第二次爬取时使用 重要性：中<br>
base_tiezi_info_ddl -> 主页中提取到的全部信息 重要性：高<br>

### 第二部分的表：

tiezi_scan -> 帖子详细内容的扫描信息 重要性：低<br>
tiezi_content_info -> 帖子主要内容信息 重要性：最高<br>
louzhonglou_info -> 楼中楼回复信息 重要性：很高<br>
image_info -> 帖子主要回复中出现的图片链接 重要性：中<br>
emoji_info -> 帖子中和楼中楼中出现的表情 重要性：中<br>
emoji_louzhonglou_relationship -> 表情和楼中楼联系 重要性：中低<br>
emoji_tiezi_content_relationship -> 表情和帖子内容联系 重要性：中低<br>

### 查询：
请见主目录下的[sqls.txt](https://github.com/yu132/Baidu-bilibili-tieba-analyse/blob/master/sqls.txt)  

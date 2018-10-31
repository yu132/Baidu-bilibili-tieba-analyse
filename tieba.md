# 本文内容
描述如何爬取百度贴吧的所有有用的内容

# 爬取对象
+ 百度贴吧指定贴吧主页（只能爬取前2000页）
+ 主页中包含的主题帖的全部页面
+ 主题帖中全部页面的楼中楼的前10条
+ 楼中楼的后续页面

# 爬取方式
## 1. 主页
#### 爬取链接：https://tieba.baidu.com/f?kw={kw}&pn={pn} (只能爬前两千)
#### 或：https://tieba.baidu.com/{kw}?"pn={pn} （可以全部爬取）

#### 参数：
+ kw: 爬取贴吧的名字
+ pn：指定第arg1条开始的后50条信息（即pn=（爬取页面的序号-1）*50）

#### 结果格式：html

## 2. 主题帖
#### 爬取连接：https://tieba.baidu.com/p/{tid}?pn={pn}

#### 参数：
+ tid:爬取帖子的id，可以从主页中获取
+ pn：页数，从1开始

#### 结果格式：html

## 3. 楼中楼前10条
#### 爬取链接：https://tieba.baidu.com/p/totalComment?t={t}&tid={tid}&fid={fid}&pn={pn}&see_lz={see_lz}

#### 参数:
+ t: 时间戳，使用当前时间即可
+ tid：帖子id，可以从主题帖或是主页上面获取
+ fid：贴吧id（猜测），每个贴吧内的帖子中对应的fid是相同的，可以从任意一个帖子中查看源码获得
+ pn：对于主题帖的页面，主题帖总共有几页，这里也要爬几页
+ see_lz： 应该是只看楼主，一般设置成0，即全部都查看

#### 结果格式：json

## 4. 爬取楼中楼后续页面
#### 爬取链接：https://tieba.baidu.com/p/comment?tid={tid}&pid={pid}&pn={pn}&t={t}

#### 参数:
+ tid：帖子id：上面提到了
+ pid：回复id，每个一回复有一个id，从楼中楼前10条信息中可以获取
+ pn：楼中楼页数，楼中楼的页数，每10个楼中楼为一页
+ t：时间戳，当前时间的就可以

#### 结果格式：html




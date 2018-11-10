# -*- coding: utf-8 -*-
import scrapy
import time
import json

import sys

sys.path.append('baiduTieba/spiders/')

import file_path
import sql_executor


now_mp_id_query="""SELECT MAX(mp_id) FROM main_page_info"""

mp_ans=sql_executor.query(now_mp_id_query)

if mp_ans[0][0]:
    now_mp_id=mp_ans[0][0]
else:
    now_mp_id=0

def extract_context_from_html_and_save(response):
 
    lis=response.css('li.j_thread_list')

    for li in lis:

        try:
            reply_num=li.css('span.threadlist_rep_num::text').extract_first()

            
            temp=li.css('div.threadlist_title').css('a')

            href=temp.css('::attr(href)')

            tid=href.re('/p/(.*)')[0]

            link=href.extract_first()

            title=temp.css('::text').extract_first()

            temp=li.css('span.tb_icon_author')
                        
            author_name=temp.css('::attr(title)').re('主题作者: (.*)')[0]

            author_home_page_link=temp.css('a::attr(href)').extract_first()

        except:
            raise RuntimeError('page prase error')

        # if it has been download before, don't save it again
        sql="""SELECT tz_id FROM tiezi_info WHERE tid=%s"""

        args=[tid]

        query_ans=sql_executor.query(sql,args)
        
        if len(query_ans):
            if len(query_ans[0]):
                if query_ans[0][0]:       
                    continue
                
        try:
            summary=li.css('div.threadlist_abs::text').extract_first().strip()
            
        except:
            summary=None

        try:
            temp=li.css('span.tb_icon_author_rely')

            replier_name=temp.css('::attr(title)').re('最后回复人: (.*)')[0]

            replier_home_page_link=temp.css('a::attr(href)').extract_first()

        except:
            replier_name=None
            replier_home_page_link=None

        """tiezi_base_info={'reply_num':reply_num,'link':link,'title':title,'author_name':author_name,
              'author_home_page_link':author_home_page_link,'summary':summary,'replier_name':replier_name,
              'replier_home_page_link':replier_home_page_link}

        json_str = json.dumps(tiezi_base_info)

        file_path.mkdir(file_path.teizi_path+'/'+tid)

        with open(file_path.teizi_path+'/'+tid+'/'+'main_page_tiezi_info.txt','w') as file:
            file.write(json_str)"""

        #insert base tiezi info
        sql="""INSERT INTO `base_tiezi_info` VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        args=[tid,reply_num,link,title,author_name,author_home_page_link,
              summary,replier_name,replier_home_page_link]
        
        sql_executor.execute_update(sql,args)

        
        #insert tiezi id and scan info
        sql="""INSERT INTO `tiezi_info` VALUES(%s,%s,%s,%s)"""

        args=[None,tid,now_mp_id,None]

        sql_executor.execute_update(sql,args)


class BaiduTiebaMainPageSpider(scrapy.Spider):
    name = "baidu_spider"

    def start_requests(self):
        urls = [
            'https://tieba.baidu.com/bilibili'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_first)

    def parse_first(self,response):
        global now_mp_id
        pn_max=response.css('a.last.pagination-item::attr(href)').re("pn=(.*)")[0]
        page_max=(int(pn_max)-1)//50+1

        time_now=int(round(time.time()*1000))

        sql="""INSERT INTO `main_page_info` VALUES(%s,%s,%s)"""
        args=[None,time_now,page_max]

        sql_executor.execute_update(sql,args)

        now_mp_id+=1

        #save page 1
        extract_context_from_html_and_save(response)
      
        #yeild other many pages which call back = parse_normal
        for page in range(1,page_max+1):
            url='https://tieba.baidu.com/bilibili?pn='+str(page*50)
            yield scrapy.Request(url=url, callback=self.parse_normal)
        

    def parse_normal(self, response):
        extract_context_from_html_and_save(response)
    

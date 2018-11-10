# -*- coding: utf-8 -*-
import scrapy
import time
import json

import sys

sys.path.append('baiduTieba/spiders/')

import file_path
import sql_executor

STEP_EACH_TIEZI_SCAN=10

class BaiduTiebaMainPageSpider(scrapy.Spider):
    name = "tieba_tiezi_spider"

    def start_requests(self):
               
        tiezi_info_sql="""SELECT tid FROM tiezi_info WHERE ts_id IS NULL ORDER BY tid DESC LIMIT %s,%s"""
        args=[1,STEP_EACH_TIEZI_SCAN]

        tiezi_info_ans=sql_executor.query(tiezi_info_sql,args)

        init_ts_sql="""INSERT INTO tiezi_scan 
        (ts_id, start_time, next_start_index) VALUES(%s,%s,%s)"""

        time_now = int(round(time.time() * 1000))
        args=[None,time_now,len(tiezi_info_ans)]

        ts_id=sql_executor.insert_and_get_id(init_ts_sql,args)
        
        base_path="https://tieba.baidu.com/p/"
        
        for tid in tiezi_info_ans:
            yield scrapy.Request(url=base_path+str(tid[0]), callback=self.parse_tiezi_main_first,meta={"tid":str(tid[0]),"ts_id":ts_id})
             
        # update the next start values so it will start from right place
        update_ts_sql="""UPDATE tiezi_scan SET next_start_index=%s WHERE ts_id=%s"""
        args=[next_start_index,ts_id]

        sql_executor.execute_update(update_ts_sql,args)

    def parse_tiezi_main_first(self,response):

        tid=response.request.meta.get("tid")

        ts_id=response.request.meta.get("ts_id")
        
        # update ts_id
        sql="""UPDATE tiezi_info SET ts_id=%s WHERE tid=%s"""
        args=[ts_id,tid]

        sql_executor.execute_update(sql,args)
        
        try:
            fid=response.css("body").re("fid:'(.*?)'")[0]
        except:
            # if there is not fid in this page, then this tiezi is deleted
            return
        
        # save now page
        save_tiezi_main_page(response)
        
        try:
            max_page=int(response.css("body").re("max-page=\"(.*?)\"")[0])
        except:
            max_page=1
   
        # other main page in this tiezi           
        for page_index in range(2,max_page+1):
            args={"tid":tid,"pn":page_index}
            
            tiezi_url="https://tieba.baidu.com/p/%(tid)s?pn=%(pn)s"%args
            yield scrapy.Request(url=tiezi_url, callback=self.parse_tiezi_main_normal,meta=args)        

        see_lz="0"
        
        # get louzhonglou list
        for page_index in range(2,max_page+1):
            time_now=str(int(round(time.time()*1000)))

            args={"t":time_now,"tid":tid,"fid":fid,"pn":page_index,"see_lz":see_lz}
            
            url="https://tieba.baidu.com/p/totalComment?t=%(t)s&tid=%(tid)s&fid=%(fid)s&pn=%(pn)s&see_lz=%(see_lz)s"%args
                 
            yield scrapy.Request(url=url, callback=self.parse_louzhonglou_list,meta=args)

    def parse_tiezi_main_normal(self, response):
        #save now page
        save_tiezi_main_page(response)

    # it's not easy to get reply time from this list, so get from another url
    def parse_louzhonglou_list(self,response):
        json_data = json.loads(response.body_as_unicode())

        comment_dict=json_data["data"]["comment_list"]

        meta=response.request.meta

        tid=meta.get("tid")
        
        # if type is list, then there is no louzhonglou in this tiezi
        if type(comment_dict)==list:
            return

        for pid,value_dict in comment_dict.items():

            comment_num=value_dict["comment_num"]

            page_num=(comment_num-1)//10+1

            for pn in range(1,page_num+1):
                time_now=str(int(round(time.time()*1000)))

                args={"t":time_now,"tid":tid,"pid":pid,"pn":pn}
                
                url="https://tieba.baidu.com/p/comment?tid=%(tid)s&pid=%(pid)s&pn=%(pn)s&t=%(t)s"%args
                 
                yield scrapy.Request(url=url, callback=self.parse_longzhonglou_normal,meta=args)
           
    def parse_longzhonglou_normal(self,response):
        save_louzhonglou_normal(response)
        

def save_tiezi_main_page(response):
    tid=response.request.meta.get("tid")
    
    main_body=response.css("div.l_post")

    # each floor
    for each_floor in main_body:

        # pid my be not exists
        try:
            pid=json.loads(each_floor.css("div.j_lzl_r::attr(data-field)").extract_first())["pid"]
        except:
            pid=None

        # author
        try:
            author=each_floor.css("div.d_author")
        except:
            author=None

        a_tag=author.css("a.p_author_name")

        try:
            author_name=a_tag.css("::text").extract_first()
        except:
            author_name=None

        try:
            author_link=a_tag.css("::attr(href)").extract_first()
        except:
            author_link=None

        if len(author_link)>255:
            author_link=None

        try:
            author_level=author.css("div.d_badge_lv::text").extract_first()
        except:
            author_level=None

        # main content
        main_content=each_floor.css("div.d_post_content")

        try:
            text=main_content.css("::text").extract()[0].strip()
        except:
            text=None

        try:
            emoji_img_list=main_content.css("img.BDE_Smiley::attr(src)").extract()
        except:
            emoji_img_list=[]

        try:
            normal_img_list=main_content.css("img.BDE_Image::attr(src)").extract()
        except: 
            normal_img_list=[]

        # tail-info
        tail_info_list=each_floor.css("span.tail-info")

        client_type=None

        try:
            for tail_info in tail_info_list:
                if tail_info.css("::text").extract_first()=='来自':
                    client_type=tail_info.css("a::text").extract_first()
        except:
            pass

        try:
            floor=tail_info_list.css("::text").re("(.*?)楼")[0]
        except:
            floor=None

        try:
            reply_time=tail_info_list.css("::text").re("....-..-.. ..:..")[0]
        except:
            reply_time=None

        # save main content info and text
        sql="""INSERT INTO tiezi_content_info 
        (content_id,
        pid,
        tid,
        author_name,
        author_level,
        author_home_page_link,
        content,
        FLOOR,
        TIME,
        client_type)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        args=[None,pid,tid,author_name,author_level,author_link,text,floor,reply_time,client_type]

        tiezi_content_id=sql_executor.insert_and_get_id(sql,args)
        
        # save image and emoji
        sql="""INSERT INTO image_info 
        (image_id,
        src,
        tid,
        pid,
        tiezi_content_id)
        VALUES (%s, %s, %s, %s, %s)"""
        
        for img_src in normal_img_list:
            args=[None,img_src,tid,pid,tiezi_content_id]
            sql_executor.execute_update(sql,args)

        sql="""INSERT INTO emoji_info 
        (emoji_id,
        src,
        word)
        VALUES (%s, %s, %s)"""

        sql_select="""SELECT emoji_id FROM emoji_info WHERE src=%s"""

        sql2="""INSERT INTO emoji_tiezi_content_relationship 
        (emoji_tiezi_content_relationship_id,
        tiezi_content_info_id,
        emoji_id)
        VALUES (%s, %s, %s)"""

        for meoji_src in emoji_img_list:

            res=sql_executor.query(sql_select,[meoji_src])
            
            if res:
                id_=res[0][0]
            else:
                args=[None,meoji_src,None]
                id_=sql_executor.insert_and_get_id(sql,args)

            args=[None,tiezi_content_id,id_]
            sql_executor.execute_update(sql2,args)


def save_louzhonglou_normal(response):
    lzl_floor_list=response.css("li.lzl_single_post")

    meta=response.request.meta

    tid=meta.get("tid")
    pid=meta.get("pid")

    for lzl_floor in lzl_floor_list:
        try:
            name=lzl_floor.css("a.j_user_card::text").extract_first()
        except:
            name=None

        content_a=lzl_floor.css("span.lzl_content_main")

        try:
            content_list=content_a.css("::text").extract()

            content=""
            
            for str_ in content_list:
                content+=str_.strip()+" "
                
        except:
            content=None

        try:
            emoji_img_list=content_a.css("img.BDE_Smiley::attr(src)").extract()
        except:
            emoji_img_list=[]

        try:
            reply_time=lzl_floor.css("span.lzl_time::text").extract_first()
        except:
            reply_time=None

        sql="""INSERT INTO tieba_spider.louzhonglou_info 
        (louzhonglou_id,
        tid,
        pid,
        author_name,
        content,
        TIME
        )
        VALUES (%s, %s, %s, %s, %s, %s)"""

        args=[None,tid,pid,name,content,reply_time]

        lzl_id=sql_executor.insert_and_get_id(sql,args)

        sql="""INSERT INTO emoji_info 
        (emoji_id,
        src,
        word)
        VALUES (%s, %s, %s)"""

        sql_select="""SELECT emoji_id FROM emoji_info WHERE src=%s"""

        sql2="""INSERT INTO tieba_spider.emoji_louzhonglou_relationship 
        (emoji_louzhonglou_relationship_id,
        louzhonglou_id,
        emoji_id)
        VALUES (%s, %s, %s)"""

        for meoji_src in emoji_img_list:
            res=sql_executor.query(sql_select,[meoji_src])

            if res:
                id_=res[0][0]
            else:
                args=[None,meoji_src,None]
                id_=sql_executor.insert_and_get_id(sql,args)

            args=[None,lzl_id,id_]
            sql_executor.execute_update(sql2,args)

    

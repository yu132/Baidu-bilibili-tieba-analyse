# -*- coding: utf-8 -*-
import os

base_path=os.environ['HOME']+"/baidu_tieba_spider"

teizi_path=base_path+"/tiezi"

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

mkdir(teizi_path)

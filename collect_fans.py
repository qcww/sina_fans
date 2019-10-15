#coding=utf-8

import requests
import json
import re
import time
import math
import random

class SinaFans:

    def __init__(self):
        self.cookie = 'SINAGLOBAL=809677189468.5428.1569636646315; Ugrow-G0=e1a5a1aae05361d646241e28c550f987; login_sid_t=5c6d4c67212fb2fc3c2e7726efec8b8b; cross_origin_proto=SSL; YF-V5-G0=a5a6106293f9aeef5e34a2e71f04fae4; wb_view_log=1920*10801; _s_tentry=passport.weibo.com; Apache=9699533503834.879.1570963044658; ULV=1570963044663:5:3:1:9699533503834.879.1570963044658:1570845627339; wb_view_log_6347700867=1920*10801; WBtopGlobal_register_version=307744aa77dd5677; SSOLoginState=1570963348; wvr=6; ALF=1602500691; SUB=_2A25wp3SEDeRhGeBN71UW8C7EzTuIHXVT1eFMrDV8PUNbmtBeLU_ukW9NRHFK-IyVKVyJXogtIzufgOAkQXNN6WxA; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whk9Bz4WrpW12YAwZ3bLk4S5JpX5KzhUgL.Foq0ShMNeh5RSoM2dJLoIE5LxK-L1K5LBoBLxKBLB.2L1K2LxK.LBo.L12qcSK54e7tt; SUHB=0h1ZyLPojoA8ye; UOR=www.51testing.com,widget.weibo.com,www.baidu.com; YF-Page-G0=530872e91ac9c5aa6d206eddf1bb6a70|1570977383|1570977372; webim_unReadCount=%7B%22time%22%3A1570977471312%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A14%2C%22msgbox%22%3A0%7D'
        self.search_url = 'https://s.weibo.com/user?q=%s&Refer=weibo_user'
        self.search_fans_url = 'https://weibo.com/%s/fans?page=%s'
        self.user_index = 0
        self.sina_header =  {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Cookie':self.cookie,
        }

    def search_user_fans(self,nickname,page=1):
        search_res = self.sina_get(self.search_url % nickname)
        # print(search_res.text)
        # 匹配pageid
        mach_uid = re.search(r'u\/(\d{2,})',search_res.text)
        if mach_uid == None:
            return
        uid = re.sub(r'u\/','',mach_uid.group(0))
        fans_url = self.search_fans_url % (uid,page)
        search_fans_res = self.sina_get(fans_url)
        # mach_pid = re.search(r'(\d{2,})\/photos',search_res.text)
        # print(search_pid_url)
        mach_fans = re.findall(r'fnick=(.{1,20})&f=',search_fans_res.text)
        if '新手指南' in mach_fans:
            mach_fans.remove('新手指南')
        print(fans_url,mach_fans)
        time.sleep(3)
        print(nickname+': ','第 '+str(page)+' 页')
        if len(mach_fans) > 20:
            page += 1
            return self.search_user_fans(nickname,page)

    def get_user(self):
        user_list = ('巍岳钦禹', '攸县雪狼陶瓷小兰', '电影控控', '用户7318693177', '小宅女悟道', '大发快彡最牛', 'PraiseforParadise', '范er小疯子郭丹', '顶迷揪揪是顶顶一生粉', '我爱我家5544642231', '柒染13246', '用户6059421213', '心一笑200', '叶雨馨呀', '意志坚强的Yo呵', '用户7318938781', '用户7318938439', '宁采臣不放弃', '高伟恺', '浅笑心柔67372', '陌离丶HNTs_vf')
        if len(user_list) <= self.user_index:
            self.user_index = 1

        current_user = user_list[self.user_index]
        self.user_index += 1
        return current_user

    def start(self):
        while True:
            user_list = self.get_user()
            self.search_user_fans(user_list)
        
            

    def sina_post(self,url,data):
        r = requests.post(url, data=data, headers=self.sina_header)
        return r

    def sina_get(self,url):
        r = requests.get(url, headers=self.sina_header)
        return r

script = SinaFans()
script.start()
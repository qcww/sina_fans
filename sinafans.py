#coding=utf-8

import requests
import json
import re
import time
import math
import random
import threading
import tkinter as tk
import configparser
import os
import tkinter.messagebox
from tkinter import simpledialog

class SinaFans:

    def __init__(self,window,lb,new_fans):
        self.window = window
        self.lb = lb
        self.search_url = 'https://s.weibo.com/user?q=%s&Refer=weibo_user'
        self.search_fans_url = 'https://weibo.com/%s/fans?page=%s'
        self.user_index = 0
        self.config_file = 'config.ini'
        self.new_fans_num = 0
        self.new_fans = new_fans
        self.RUN_STATUS = True
        self.run_selec_label = '' # 存储运行中label防止脚本运行中切换lable
        
        # 读取生成配置
        self.read_config()
        self.login()
        self.collect_group = self.get_config('label','default')
        self.period = int(self.get_config('scrapy','sleep'))

        print(self.get_config('collect',self.collect_group))


    def read_config(self):
        config_file = self.config_file
        config = configparser.ConfigParser()
        if os.path.exists(config_file) == False:
            config['login'] = {'Cookie': ''}
            config['collect'] = {}
            config['collect']['默认标签'] = ''
            config['scrapy'] = {'sleep':'1','submit_url':'http://dyapi.bjbctx.com/api/weibo/addFans'}
            config['label'] = {'default':'默认标签'}

            with open(config_file, 'w+') as configfile:
                config.write(configfile)
        config.sections()
        config.read(config_file)
        self.config = config

    # 读取配置下所有options 
    def get_config_options(self,section):
        return self.config.options(section)

    # 读取 配置>option>key 的值
    def get_config(self,section,key):
        return re.sub(r'#53','%',self.config.get(section,key))

    # 写入配置
    def set_config(self,section,key,value):
        set_val = str(value)
        self.config.set(section,key,re.sub(r'%','#53',set_val.strip('|')))
        self.config.write(open(self.config_file,'w'))

    # 设置默认标签
    def set_default_label(self,label):
        # 切换标签时重置获取采集用户list的位置
        self.user_index = 0
        self.collect_group = label
        self.set_config('label','default',label)

    # 设置每轮采集的间隔
    def set_period(self,period):
        self.set_config('scrapy','sleep',period)
        self.period = int(period) 

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
        # 提交匹配的粉丝
        if(len(mach_fans) > 0):    
            self.submit_fans(mach_fans)

        for m in mach_fans:
            self.lb.insert(0,m)
        # self.lb.insert(0,current_user)
        time.sleep(3)
        print(nickname+': ','第 '+str(page)+' 页')

        if len(mach_fans) >= 10 and page < 5:
            page += 1
            return self.search_user_fans(nickname,page)

    def add_label(self,label):
        self.set_config('collect',label,'')

    def add_user_list(self,input_list):
        if input_list == '':
            return
        user_list = self.get_user_list()
        add_user = input_list.split('||')

        if len(add_user) != 0:
            user_list.extend(add_user)
            res_user = list(set(user_list))
            print(res_user)
            self.set_config('collect',self.collect_group,'||'.join(res_user))

    def get_user_list(self):
        li = self.get_config('collect',self.collect_group)
        if li == '':
            time.sleep(2)
            return []
        self.run_selec_label = self.collect_group
        tar = [str(x) for x in li.split('||')]
        return tar

    def get_user(self):
        while self.RUN_STATUS:
            user_list = self.get_user_list()

            if len(user_list) <= self.user_index:
                self.user_index = 0

            if len(user_list) == 0:
                tkinter.messagebox.showinfo(title='提示',message='请添加待采集粉丝后重试')
                return False
            else:
                current_user = user_list[self.user_index]
                self.window.title('正在采集：'+current_user)
                
                self.user_index += 1
                time.sleep(1)
                self.search_user_fans(current_user)
                time.sleep(self.period)

    # 登录
    def login(self):
        self.sina_header =  {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Cookie':self.get_config('login','Cookie'), # 读取cookie务必使用本类中方法
        }

    # 提交粉丝数据
    def submit_fans(self,mach_fans):
        submit_header =  {
            'Accept':'application/jgwl.douyin.v1+json',
            'Content-Type':'application/x-www-form-urlencoded', # 读取cookie务必使用本类中方法
        }
        data = {'group':self.run_selec_label,'fans':json.dumps(mach_fans)}
        sub = requests.post(self.get_config('scrapy','submit_url'), data, headers=submit_header)
        if sub:
            js_new = sub.json()
            self.new_fans_num += int(js_new['new'])
            self.new_fans.set('新添加粉丝： '+str(self.new_fans_num))

    def start(self):
        self.mythread = threading.Thread(target=self.get_user)
        self.cond = threading.Condition() # 锁
        self.mythread.start()
        # while True:
        #     user_list = self.get_user()
        #     self.search_user_fans(user_list)
        
            

    def sina_post(self,url,data):
        r = requests.post(url, data=data, headers=self.sina_header)
        return r

    def sina_get(self,url):
        r = requests.get(url, headers=self.sina_header)
        return r


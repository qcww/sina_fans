import requests
import json
import re

class SinaFans:

    def __init__(self):
        self.cookie = 'SINAGLOBAL=809677189468.5428.1569636646315; Ugrow-G0=cf25a00b541269674d0feadd72dce35f; login_sid_t=6985ef759a764e53943757923efb6db6; cross_origin_proto=SSL; YF-V5-G0=95d69db6bf5dfdb71f82a9b7f3eb261a; _s_tentry=passport.weibo.com; Apache=4785743699482.156.1570845627332; ULV=1570845627339:4:2:2:4785743699482.156.1570845627332:1570754660916; wb_view_log=1920*10801; WBtopGlobal_register_version=307744aa77dd5677; ALF=1602381782; SSOLoginState=1570845783; SUB=_2A25wpUQIDeRhGeBN71UW8C7EzTuIHXVT0zLArDV8PUNbmtBeLRnHkW9NRHFK-GrJJltFWM0Im0f3RvXh6XnwMWJc; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whk9Bz4WrpW12YAwZ3bLk4S5JpX5KzhUgL.Foq0ShMNeh5RSoM2dJLoIE5LxK-L1K5LBoBLxKBLB.2L1K2LxK.LBo.L12qcSK54e7tt; SUHB=0cS3m5j4rz9Je5; wvr=6; UOR=www.51testing.com,widget.weibo.com,graph.qq.com; wb_view_log_6347700867=1920*10801; YF-Page-G0=761bd8cde5c9cef594414e10263abf81|1570849425|1570849418; webim_unReadCount=%7B%22time%22%3A1570849427647%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A5%2C%22msgbox%22%3A0%7D'
        self.search_url = 'https://s.weibo.com/user?q=%E5%B7%8D%E5%B2%B3%E9%92%A6%E7%A6%B9&Refer=weibo_user'
        self.search_fans_url = 'https://weibo.com/%s/fans'
        self.sina_header =  {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Cookie':self.cookie,
        }

    def search_user_id(self):
        search_res = self.sina_get(self.search_url)
        # print(search_res.text)
        # 匹配pageid
        mach_uid = re.search(r'u\/(\d{2,})',search_res.text)
        if mach_uid == None:
            return
        uid = re.sub(r'u\/','',mach_uid.group(0))
        search_fans_res = self.sina_get(self.search_fans_url % uid)
        # mach_pid = re.search(r'(\d{2,})\/photos',search_res.text)
        # print(search_pid_url)
        print(search_fans_res.text)

    def sina_post(self,url,data):
        r = requests.post(url, data=data, headers=self.sina_header)
        return r

    def sina_get(self,url):
        r = requests.get(url, headers=self.sina_header)
        return r

script = SinaFans()
script.search_user_id()
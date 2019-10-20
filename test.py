import requests
import json

submit_header =  {
    'Accept':'application/jgwl.douyin.v1+json',
    'Content-Type':'application/x-www-form-urlencoded', # 读取cookie务必使用本类中方法
}
match_fans = ['电影神吐槽', 'XruFG牛头不对马嘴ydj_22431', '哈士奇', '二哈dd', 'PxuLs九牛二虎之力xmv_52975', '用户7323799701', '生洳此颜差矣郁钱', 'PX0rR澳门特别行政zjn_2975', 'FJ6mw横挑鼻子竖挑clv_1683', '用户7323799424', '小棉袄198112', 'pwautism', 'XruFG牛头不对马嘴syb', 'PX0rR澳门特别行政qcm', 'ZMICG醉翁之意不在mwr_22274', '半醉屠瑜丶赞', '用户7323525533', '用户6110233925', '用户7306000805', '用户7323797277']
data = {'group': '茶叶', 'fans': json.dumps(match_fans)}
url = 'http://dyapi.bjbctx.com/api/weibo/addFans'
res = requests.post(url,data=data,headers=submit_header)
print(res.text)
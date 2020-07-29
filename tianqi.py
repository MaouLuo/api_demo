# -*- coding:utf-8 -*-

import requests
import json
import re
import tools

def bad_wea(text):
    pattern = r'.*?[雨雪].*?'
    if re.search(pattern, text, flags=0):
        return True 
    return False

def get_day(text):
    pattern = r'.*?[日]'
    r = re.search(pattern, text, flags=0)
    #print(r.group())
    return r .group()

def today_bad_wea():
    title, cont = '', ''
    bwea = False
    url = 'https://tianqiapi.com/api'    
    params = {
        'version': 'v1',
        'appid': tools.r_conf('tianqi', name='appid'),
        'appsecret': tools.r_conf('tianqi', name='appsecret')
    }

    resp = requests.get(url, params=params)
    jd = json.loads(resp.text)    
    for w in jd['data'][0]['hours']:
        if bad_wea(w['wea']):
            cont += '{}，{}，{}'.format(w['day'], w['wea'], w['tem']) + '\r\n\r\n'
            bwea = True
            #title = '{} {} {}'.format(day, jd['city'], jd['data'][0]['wea'])
            #cont += '当前{}，最低{}，最高{}'.format(jd['data'][0]['tem'], jd['data'][0]['tem2'], jd['data'][0]['tem1']) + '\r\n\r\n'
    if bwea:
        day = get_day(jd['data'][0]['day'])
        title = '{} {} {}'.format(day, jd['city'], jd['data'][0]['wea'])
    else:
        cont = False
    return title, cont
    
# 用Nowapi实时天气接口，每1小时更新一次
def get_cur_wea(weaid='南山'):
    url = 'http://api.k780.com'
    data = {
        'weaid': weaid,
        'app': 'weather.realtime',
        'appkey': tools.r_conf('nowapi', name='appkey'),
        'sign': tools.r_conf('nowapi', name='sign'),
        'format': 'json'
    }
    resp = requests.post(url, data=data)
    jd = json.loads(resp.text)

    wtNm = jd['result']['realTime']['wtNm'] # 天气类型
    wtTemp = jd['result']['realTime']['wtTemp'] # 温度

    return {'wtNm':wtNm , 'wtTemp':wtTemp}


def main():
    title, cont = today_bad_wea()
    if cont:
        sj = tools.ServerJ(title=title, cont=cont , token=tools.r_conf('sj'), debug=True)
        sj.run()
    else:
        print('good wea')

if __name__ == '__main__':
    main()
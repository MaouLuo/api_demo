# -*- coding:utf-8 -*-

import requests
import json
import re
import configparser 
from serverj import ServerJ

# 读取配置文件函数
# os.path.dirname(os.path.realpath(__file__)))获取当前路径，os.getcwd()获取有异常，仅能拿到1级目录
def r_conf(item, path='D:\\code'+'\\config.ini', name='token'):
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    cont = config.get(item, name)
    #print(cont)
    return cont

def bad_wea(text):
    pattern = r'.*?[雨雪].*?'
    if re.search(pattern, text, flags=0):
        return True 
    #print('none')
    return False

def today_bad_wea():
    cont = ''

    url = 'https://tianqiapi.com/api'    
    params = {
        'version': 'v1',
        'appid': r_conf('tianqi', name='appid'),
        'appsecret': r_conf('tianqi', name='appsecret')
    }

    resp = requests.get(url, params=params)
    jd = json.loads(resp.text)
    for w in jd['data'][0]['hours']:
        if bad_wea(w['wea']):
            #print('{}，{}，{}'.format(w['day'], w['wea'], w['tem']))
            cont += '{}，{}，{}'.format(w['day'], w['wea'], w['tem']) + '\r\n'
    if cont:
        return cont
    return False

def main():
    cont = today_bad_wea()
    if cont:
        sj = ServerJ(title='天气预警', cont=cont , token=r_conf('sj'), debug=False)
        sj.run()

if __name__ == '__main__':
    main()
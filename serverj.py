# -*- coding:utf-8 -*-

import requests
import time
import configparser 
import os
import datetime

# 通过server酱发送公众号消息。每分钟相同内容只能发一次，相同内容包括标题和正文
# 调试模式仅打印不发微信
class ServerJ:
    def __init__(self, title, cont, token, debug=True): 
        self.url = 'https://sc.ftqq.com/'
        self._token = token
        self.title = title
        self.cont = cont
        self.debug = debug
  
    def check(self):
        title, cont = False, False
        print('title:{},\r\n cont:{}'.format(self.title, self.cont))
        if self.title:
            title = self.title
        if self.cont:
            cont = self.cont
        return {'title':title, 'cont':cont}

    def run(self):
        if self.cont is False:
            cont = 'No Data.'
        else:
            cont = self.cont
        
        data = {
            'text': self.title, # 消息标题，最长为256，必填
            'desp': cont # 消息内容，最长64Kb，可空，支持MarkDown。
        }
        if self.debug is True:
            print(data)
        else:
            try:
                resp = requests.post(self.url+self._token, data=data)
            except:
                print(resp.text)
        return True
# -*- coding:utf-8 -*-
import tushare as ts
#import requests
import time
import configparser 
import os
import datetime
import sqlite3
from sqlalchemy import create_engine 

engine_ts = create_engine('mysql://root:abc123@127.0.0.1:3306/shares?charset=utf8&use_unicode=1')


# 读取配置文件函数
# os.path.dirname(os.path.realpath(__file__)))获取当前路径，os.getcwd()获取有异常，仅能拿到1级目录
# def r_conf(item, path=os.path.dirname(os.path.realpath(__file__))+'\\config.ini', name='token'):
def r_conf(item, path='D:\\code'+'\\config.ini', name='token'):
    #print('{} {} {}'.format(item, path, name))
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    cont = config.get(item, name)
    #print(cont)
    return cont

# 获取日期
def get_date():
    cur_time = datetime.datetime.now()
    date = cur_time.strftime("%Y%m%d")
    #print(date-1)
    return date

class Shares():
    def __init__(self):
        self.token = r_conf('ts')
        self.pro = ts.pro_api()
        
    # 获取交易日历，默认ssh深交所，默认显示交易日
    def get_cal(self, sdate, edate, exc='sse', is_open='1'):
        df = self.pro.trade_cal(start_date=sdate, end_date=edate, exchange=exc, is_open=is_open)
        #df = pro.trade_cal(exchange=exc, start_date='20180101', end_date='20180231')
        #print(df)
        return df

def write_data(df):
    res = df.to_sql('cal', engine_ts, index=False, if_exists='replace', chunksize=5000)
    print(res)

def main():
    share = Shares()
    df = share.get_cal('20100101', '20200111')
    write_data(df)

if __name__ == '__main__':
    main()
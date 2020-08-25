# -*- coding:utf-8 -*-
import tushare as ts
#import requests
from time import *
import sqlite3
import tools
import trade_date

debug_path = 'D:\\code\\api_demo\\tushare\\ts_test.db'
release_path = 'D:\\code\\api_demo\\tushare\\shares.db'
path = debug_path

def get_open_date(table_name, filed_name, value):
    date = []
    cal_db = trade_date.shares_db(path)
    res = trade_date.query(cal_db, table_name, filed_name, value)
    for day in res:
        date.append(trade_date=day[1])
    return date

def query(table_name):
    cal_db = trade_date.shares_db(path)
    res = trade_date.query(cal_db, table_name, filed_name, value)
    print(res)


class Shares():
    def __init__(self):
        self.token = tools.r_conf('ts')
        self.pro = ts.pro_api()
        
    # 获取交易日历，默认ssh深交所，默认显示交易日
    def get_cal(self, sdate, edate, exc='sse', is_open='1'):
        df = self.pro.trade_cal(start_date=sdate, end_date=edate, exchange=exc, is_open=is_open)
        #df = pro.trade_cal(exchange=exc, start_date='20180101', end_date='20180231')
        #print(df)
        return df

    def all_daily(self, date):
        
        #res = get_open_date('cal', 'is_open', '1')        
        for d in date:
            db = trade_date.shares_db(path)
            df = self.pro.daily(trade_date=d) # 0交易所，1日期，2交易日
            db.insert_data('daily', df)      #  ts_code     trade_date  open  high   low  close  pre_close  change    pct_chg  vol        amount
            sleep(0.2)  

def main():
    share = Shares()
    #open_date = get_open_date('cal', 'is_open', '1')
    open_date = ['20200817']#, '20200818', '20200819', '20200820', '20200821']
    share.all_daily(open_date)
    #df = share.get_cal('20100101', '20200111')
    #share.daily('20200821')
    #print(df)
    query()

if __name__ == '__main__':
    main()
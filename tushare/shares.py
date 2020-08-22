# -*- coding:utf-8 -*-
import tushare as ts
#import requests
import time
import sqlite3
import tools
import trade_date

debug_path = 'D:\\code\\api_demo\\tushare\\ts_test.db'
release_path = 'D:\\code\\api_demo\\tushare\\shares.db'
path = debug_path

def get_open_date(table_name, filed_name, value):
    cal_db = trade_date.shares_db(path)
    res = trade_date.query(cal_db, table_name, filed_name, value)
    return res

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
        db = trade_date.shares_db(path)
        #res = get_open_date('cal', 'is_open', '1')        
        for d in date:
            df = self.pro.daily(trade_date=d[1])
            db.insert_data('daily', df)
        

def main():
    share = Shares()
    open_date = get_open_date('cal', 'is_open', '1')
    share.all_daily(open_date)
    #df = share.get_cal('20100101', '20200111')
    #share.daily('20200821')
    #print(df)

if __name__ == '__main__':
    main()
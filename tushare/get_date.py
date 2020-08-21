# -*- coding:utf-8 -*-

import tushare as ts
import sqlite3
import tools

debug_path = 'D:\\code\\api_demo\\tushare\\date.db'
release_path = 'D:\\code\\api_demo\\tushare\\open_cal.db'

class Deal_db():    
    def __init__(self):
        self.conn = sqlite3.connect(release_path)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('create table date (date varchar(20))')

    def commit(self):
        # 关闭Cursor:
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    def insert_data(self, date):
        try:
            for d in date:
                self.cursor.execute('insert into date (date) values (\'{}\')'.format(d))
        except:
            print('insert data error')
        finally:
            self.commit()    

    def query_all(self):
        try:
            self.cursor.execute("select * from date ")
            res = self.cursor.fetchall()
            #for i in res:
            #    print(i[0])
            print(res)
        except:
            print('query data error')
        finally:
            self.commit() 

    def check_date(self):
        try:
            self.cursor.execute("select * from date ")
            res = self.cursor.fetchall()
            print(res)
        except:
            print('query data error')
        finally:
            self.commit() 

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

def main():
    share = Shares()
    df = share.get_cal('20200101', '20200111')
    print(df)
    #date = ['20180921']
    #db = Deal_db()
    #db.create_table()
    #db.insert_data(date)  

    #db1 = Deal_db()
    #db1.query_all()    

if __name__ == "__main__":
    main()
# -*- coding:utf-8 -*-

import tushare as ts
import sqlite3
import tools
import pandas as pd
from time import *

debug_path = 'D:\\code\\api_demo\\tushare\\ts_test.db'
release_path = 'D:\\code\\api_demo\\tushare\\trade_cal.db'

class Deal_db():    
    def __init__(self):
        self.conn = sqlite3.connect(release_path)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('create table cal (exc varchar(10) date varchar(10), open varchar(10))')        

    def commit(self):
        # 关闭Cursor:
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    def insert_data(self, data): # df['cal_date'].values, df['is_open'].values        
        #for d in date:
        #    self.cursor.execute('insert into cal (date, open) values (\'{}\', \'{}\')'.format(d, open))
        data.to_sql('cal', con=self.conn, if_exists='append', index=False) # 复制dataframe数据入数据库， if_exists='append'为添加数据模式 

    def query_all(self):        
        #self.cursor.execute("select * from cal ") # 查询表下所有数据
        self.cursor.execute('select count(*) from cal') # 查询表下所有数据量
        res = self.cursor.fetchall()
        #for i in res:
        #    print(i[0])
        print(res)        

    def open_check(self):        
        self.cursor.execute("select * from cal where cal_date=20200722")
        #self.cursor.execute('select count(*) from date')
        res = self.cursor.fetchall()
        print(res)

    def duplicate_data(self): # 查询重复数据，cal为表名,cal_date为字段名
        self.cursor.execute("select * from cal group by cal_date having count(*)>1")
        res = self.cursor.fetchall()
        print(res)
        
    def del_duplicate(self): # 删除重复数据       
        self.cursor.execute("delete from cal where cal.rowid not in (select MAX(cal.rowid) from cal group by cal_date);")
        #res = self.cursor.fetchall()
        #print(res)


class Shares():
    def __init__(self):
        self.token = tools.r_conf('ts')
        self.pro = ts.pro_api()
        
    # 获取交易日历，默认ssh深交所，默认显示交易日/ 返回exchange  cal_date  is_open
    def get_cal(self, sdate, edate, exc='sse', is_open='0'):
        df = self.pro.trade_cal(start_date=sdate, end_date=edate, exchange=exc)        
        #print(df)
        return df

def insert():
    #writer = pd.ExcelWriter('./date_text.xlsx')
    share = Shares()
    db = Deal_db()

    days = [['19910101', '20001231'], ['20010101', '20101231'], ['20110101', '20201231']]
    #day1 = [['20200701', '20200801']]
    
    try:
        for d in days:
            s = time()
            df = share.get_cal(d[0], d[1])
            db.insert_data(df)

            #df.to_excel(writer, sheet_name = d[0], index = True) 
            sleep(1)
            e = time()
            print('{}秒'.format(e-s))
    except Exception as e:
        print('bad insert {}'.format(e))
    else:
        print('good insert')
    finally:
        db.commit()
        #writer.save()
        #writer.close()
        pass
    
def query():    
    db = Deal_db()
    try:
        db.del_duplicate()
        db.query_all()
        db.open_check()
        db.duplicate_data()
    except Exception as e:
        print('query data error {}'.format(e))
    finally:
        db.commit()     

def create():
    db = Deal_db()
    try:
        db.create_table()
    except Exception as e:
        print('create error {}'.format(e))
    finally:
        db.commit()  

def main():
    #create() 已无用
    #insert()
    query()

if __name__ == "__main__":
    main()
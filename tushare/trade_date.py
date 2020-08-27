# -*- coding:utf-8 -*-

import tushare as ts
import sqlite3
import tools
import pandas as pd
from time import *

debug_path = 'D:\\code\\api_demo\\tushare\\ts_test.db'
release_path = 'D:\\code\\api_demo\\tushare\\stock.db'
path = release_path

class shares_db():    
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
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

    def insert_data(self, table_name, data): # df['cal_date'].values, df['is_open'].values        
        #for d in date:
        #    self.cursor.execute('insert into cal (date, open) values (\'{}\', \'{}\')'.format(d, open))
        data.to_sql(table_name, con=self.conn, if_exists='append', index=False) # 复制dataframe数据入数据库， if_exists='append'为添加数据模式 

    def query_all(self, table_name):        
        #self.cursor.execute("select * from cal ") # 查询表下所有数据
        self.cursor.execute('select count(*) from {}'.format(table_name)) # 查询表下所有数据量
        res = self.cursor.fetchall()
        #for i in res:
        #    print(i[0])
        print(res)        

    def open_check(self, table_name, filed_name, value):        
        self.cursor.execute("select * from {} where {}={}".format(table_name, filed_name, value))
        #self.cursor.execute('select count(*) from date')
        res = self.cursor.fetchall()
        return res

    def duplicate_data(self, table_name, filed_name): # 查询重复数据，cal为表名,cal_date为字段名
        self.cursor.execute("select * from {} group by {} having count(*)>1".format(table_name, filed_name))
        res = self.cursor.fetchall()
        print(res)
        
    def del_duplicate(self, table_name, filed_name): # 删除重复数据       
        self.cursor.execute("delete from {} where {}.rowid not in (select MAX({}.rowid) from {} group by {});".format(table_name, table_name, table_name, table_name, filed_name))
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

    def get_list(self):
        df = self.pro.stock_basic(exchange='', list_status='L')
        #print(shares_list)
        return df

def insert(table_name):
    #writer = pd.ExcelWriter('./date_text.xlsx')
    share = Shares()
    db = shares_db(path)

    days = [['19910101', '20001231'], ['20010101', '20101231'], ['20110101', '20201231']]
    day1 = [['20200701', '20200801']]
    
    try:
        for d in day1:
            s = time()
            df = share.get_cal(d[0], d[1])
            db.insert_data(table_name, df)

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

def insert_list(table_name):
    #writer = pd.ExcelWriter('./date_text.xlsx')
    share = Shares()
    db = shares_db(path)
      
    try:
        shares_list = share.get_list()
        db.insert_data(table_name, shares_list)
    except Exception as e:
        print('bad list insert {}'.format(e))
    else:
        print('good list insert')
    finally:
        db.commit()
        #writer.save()
        #writer.close()

def query_all(db, table_name):
    #db = shares_db(path)
    db.query_all(table_name)
    db.commit()
    
def query(db, table_name, filed_name, value):    
    
    try:
        #db.del_duplicate(table_name, filed_name)
        db.query_all(table_name)
        res = db.open_check(table_name, filed_name, value)
        #db.duplicate_data(table_name, filed_name)
    except Exception as e:
        print('query data error {}'.format(e))
    finally:
        db.commit()  
        return res   

def create():
    db = shares_db(path)
    try:
        db.create_table()
    except Exception as e:
        print('create error {}'.format(e))
    finally:
        db.commit()  

def main():
    #create() 已无用
    ''' 获取交易日历 
    insert('cal')
    db = shares_db(path)
    res = query(db, 'cal', 'is_open', '1')
    open_date = [d[1] for d in res]
    print(open_date)
    '''
    insert_list('stock_list')


if __name__ == "__main__":
    main()
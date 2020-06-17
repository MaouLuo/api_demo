# -*- coding:utf-8 -*-
import tushare as ts
import requests
import time
import configparser 
import os
import datetime


# 读取配置文件函数
# os.path.dirname(os.path.realpath(__file__)))获取当前路径，os.getcwd()获取有异常，仅能拿到1级目录
def r_conf(item, path=os.path.dirname(os.path.realpath(__file__))+'\\config.ini', name='token'):
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


# 600887伊利 601111中国国行  601555东吴证券
shares = {'600887.SH':'伊利股份', '601111.SH':'中国银行', '601555.SH':'东吴证券'}

# 从tushare取数据，返回格式为列表,内部数据对象为字典
class Tushare:
    def __init__(self):
        # tushare token
        self.token = r_conf('ts')
        #print(type(self.token))
        ts.set_token(self.token)
        self.data = []
        self.content = False

    def today(self):
        data = []
        for k,v in shares.items():

            date = get_date()
            # 前复权行情
            try:
                df = ts.pro_bar(ts_code=k, adj='qfq', start_date=date, end_date=date)
                #print(df)
                if df is None or df.empty is True:
                    continue                
            except Exception as e:
                print('tushare数据获取失败', k, e)

            # 读取第0行‘amount’字段值，a = df['amount'][0]同此 // a=('%.2f' %b) a从b中取值2位小数
            high = ('%.2f' %df.loc[0, 'high']) # 最高价
            low = ('%.2f' %df.loc[0, 'low']) # 最低价
            close = ('%.2f' %df.loc[0, 'close']) # 收盘价
            pct_chg = ('%.2f' %df.loc[0, 'pct_chg']) # 涨跌幅
            data.append({v:{'date':date,'high':high, 'low':low, 'close':close, 'pct_chg':pct_chg}})
        return data
            
    def data_print(self, data):
        for d in data:
            for k,v in d.items():
                print('{0} 今日最高{1}，最低{2}，收盘{3}，涨幅{4}%'.format(k, v['high'], v['low'], v['close'], v['pct_chg']))
        return True

    def cont_processing(self):
        content = ''
        for d in self.data:
            for k,v in d.items():
                content += '### ' + k + '\r\n' + '最高{0}，最低{1}，收盘{2}，涨幅{3}%'.format(v['high'], v['low'], v['close'], v['pct_chg']) + '\r\n'
        return content

    def run(self):
        self.data = self.today()
        if self.data:
            self.content = self.cont_processing()
        #print(self.data)
        #print(self.content)
        return self.content        

# 通过server酱发送公众号消息。每分钟相同内容只能发一次，相同内容包括标题和正文
# 调试模式仅打印不发微信
class ServerJ:
    def __init__(self, title, cont, debug=True): 
        self.url = 'https://sc.ftqq.com/'
        self._token = r_conf('sj')
        self.title = title
        self.cont = cont
        self.debug = debug
  
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


def main():
	#pct_chg = tushare() 
	#sever_test(cont=pct_chg)
    
    '''
    print (os.getcwd())
    print (sys.argv[0])
    print(os.path.dirname(os.path.realpath(__file__)))
    '''
    tstarget = Tushare()
    cont = tstarget.run()
    
    sj = ServerJ('今日关注', cont)
    sj.run()
    

if __name__ == '__main__':
    main()
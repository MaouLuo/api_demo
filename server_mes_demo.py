# -*- coding:utf-8 -*-
import tushare as ts
import requests
import time

token = 'fe2c01954a77bf035de64e5e29a54c9835bd6da208986a156f3fde56'
# ts.set_token('305399e563d2a2ae6b48efe5ec38eeeea11599aca8c7d77816a2baa1')

def tushare():
	ts.set_token(token)

    #取000001的前复权行情
	df = ts.pro_bar(ts_code='600887.SH', adj='qfq', start_date='20200608', end_date='20200608')
    #print(df.loc[0, 'amount'])

    # 读取第0行‘amount’字段值，a = df['amount'][0]同此 // a=('%.2f' %b) a从b中取值2位小数
	a = ('%.2f' %df.loc[0, 'pct_chg']) 
	return a


# 每分钟相同内容只能发一次，相同内容包括标题和正文
def sever_test(cont, title='今日涨幅'):
	url = 'https://sc.ftqq.com/SCU77831Td9cccdfd533462659d8d881e9408da945e1ffad3eb8a8.send'
	data = {
		'text': title, # 消息标题，最长为256，必填
        'desp': cont # 消息内容，最长64Kb，可空，支持MarkDown。
	}
	resp = requests.post(url, data=data)
	print(resp.text)

def main():
	pct_chg = tushare()
	sever_test(cont=pct_chg)


if __name__ == '__main__':
    main()
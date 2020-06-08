import tushare as ts


token = 'fe2c01954a77bf035de64e5e29a54c9835bd6da208986a156f3fde56'
# ts.set_token('305399e563d2a2ae6b48efe5ec38eeeea11599aca8c7d77816a2baa1')
ts.set_token(token)
#pro = ts.pro_api(token)

# df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
# print(df)

def test():
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    print(data)

def general():
    #取000001的前复权行情
    df = ts.pro_bar(ts_code='600887.SH', adj='qfq', start_date='20200608', end_date='20200608')
    #print(df.loc[0, 'amount'])

    # 读取第0行‘amount’字段值，a = df['amount'][0]同此 // a=('%.2f' %b) a从b中取值2位小数
    a = ('%.2f' %df.loc[0, 'pct_chg']) 

    print(a)

def main():
    general()

if __name__ == '__main__':
    main()
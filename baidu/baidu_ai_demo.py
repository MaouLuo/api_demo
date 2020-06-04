# -*- coding:utf-8 -*-

import requests
import json

def get_token():
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    
    params = { 'grant_type' : 'client_credentials',           
                'client_id' : 'VyGvFxOAqATnyFfLYLIK52j9',          
                'client_secret': 'm43vGXGqSUbQyjL2hMP68cEqG9t4b7R8'     }          # 输出结果设置为json格式
    resp = requests.post(url, params=params)
    jd = json.loads(resp.text)
    #print(jd['access_token'])
    return jd['access_token']


t = '跨境电商 | 美国暴乱升级，亚马逊关闭部分运营点，配送恐受影响！”'

x= '''
近日，美国各地爆发了抗议活动，弗洛伊德案所引发的民愤呈现出升级态势，抗议活动席卷全美至少75座城市，各地的抗议活动总计有数万人参加。
印第安纳波利斯市当天出现多起枪击事件，造成一人死亡。底特律陷入混乱，一名19岁青年中弹身亡。芝加哥再次发生焚烧国旗事件，约3000名抗议者集结在当地的特朗普国际酒店进行示威。
纽约数千名示威者连续第三天走上街头，有视频显示，一辆警车被围堵后突然加速冲撞人群，这一行为瞬间激怒周围的示威者；在密苏里州圣路易斯市，一名疑似为抗议者的男子被联邦快递卡车撞死。
美国多地出现袭警事件。5月30日，费城至少13名警员被殴打致伤，4辆警车被当街焚毁；盐湖城的一名警员被球棒击中头部；佛罗里达州一名警员颈部被割伤。
暴乱在不断地升级，但特朗普没有起到领导作用，他做的似乎只有一件事：发推特。
亚马逊也不得不关闭一部分配送中心来确保安全……
据外媒报道，由于美国各地暴发大规模的示威游行和骚乱，亚马逊正在缩减其芝加哥等少数城市的快递业务，关闭部分送货运营点，并对一些送货路线作出调整。
亚马逊一位发言人向彭博社表示，“我们正在密切监视形势，在少数几个城市，我们调整了业务路线，或者缩减了常规的业务，以确保我们团队人员的安全。”
亚马逊表示：“我们与当地官员保持密切联系，并将继续监视抗议活动。” “我们正在积极监控每个地区的游行情况，并正在重新规划送货路线，以确保送货路线是安全的。”  
据外媒报道，亚马逊还于周六向在芝加哥和洛杉矶的亚马逊送货司机发送了一则通知，通知称：“如果你现正在送货，立即停下来回家。如果你的送货任务还没有完成，请返回并且将未交付的包裹交还到取货的位置。”通知已发送给包括明尼阿波利斯，西雅图，洛杉矶，纳什维尔和迈阿密在内的近十二个城市的司机。
跨境电商 | 美国暴乱升级，亚马逊关闭部分运营点，配送恐受影响！
通知中提到，亚马逊表示已关闭“靠近游行示威活动”的送货地点，并在确认安全后将重新打开这些地点。  
亚马作出这样的举措其实是有原因的，美国加州圣莫尼卡，抗议示威者抢劫了一辆亚马逊送货车，现在抗议示威者打着抗议的幌子去明目张胆的抢劫，亚马逊不得不关闭一些配送中心、减少货车送货，只有这样才能减少损失。
若是暴乱持续升级，亚马逊会关闭更多的配送中心以确保安全，这对订单的配送影响十分严重，而且暴乱还会影响消费者的购买欲望，卖家定要做好近几天单量惨淡的准备。 
当然还有卖家担心抗议者会去亚马逊仓库纵火烧了自己的货，卖家的担心不无道理，如果亚马逊仓库的货被烧了，卖家还要费事儿去补货，而且物流渠道也不顺畅，所以卖家才有了这样的担忧。 
不过有卖家表示，根本不用害怕的，如果货真的被烧了，亚马逊是会赔偿的，和卖出去一样，那些卖不出去的货还不如被烧了拿赔偿，不用太过担心。
'''


def get_content(url):
    resp = requests.get(url)
    print(resp.text)


def keyword(token):
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/keyword' 
    headers = {'Content-Type': 'application/json'}
    params = {'access_token': token,
                'charset': 'UTF-8'                    }
    data = {'title': t,
                'content': x}
    resp = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    jd = json.loads(resp.text)
    print(jd)



def news_summary(token):
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/news_summary' 
    headers = {'Content-Type': 'application/json'}
    params = {'access_token': token                  }
    data = { 'title': '一个美国硅谷VC讲述后悔错过投资“抖音”的真实故事',
            'content': x,
            'max_summary_len':200}
    resp = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    jd = json.loads(resp.text)
    print(jd)


def simnet(token):
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet' 
    headers = {'Content-Type': 'application/json'}
    params = {'access_token': token,
                'charset': 'UTF-8'                  }
    data = { 'text_1': '太阳',
            'text_2': '你好' }
    resp = requests.post(url, params=params, headers=headers, data=json.dumps(data))
    jd = json.loads(resp.text)
    print(jd)




def main():
    token = get_token()
    keyword(token)
    #news_summary(token)
    #simnet(token)
    url = 'http://www.sofreight.com/news_45624.html'
    #get_content(url)

if __name__ == '__main__':
    main()




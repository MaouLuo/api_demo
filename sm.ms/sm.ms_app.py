import requests
import json
from bs4 import BeautifulSoup as bs

# 一小时内上传历史
def history():
    url = 'https://sm.ms/api/list'    
    res = requests.get(url)
    
    jd = json.loads(res.text)                 # 将json格式转化为Python字典
    if jd['code'] == 'success':
        print(jd)
        # data = {'timestamp': jd['data'][0]['timestamp']}
        # print(data)
    return True

# 上传图片 无法上传含中文名图片，会报错：No files were uploaded. 与request有关
def upload(img_path):
    url = 'https://sm.ms/api/upload'      
    file = {'smfile': open(img_path, 'rb')}     # smfile为表单名称。上传图片用到
    res = requests.post(url, files = file )  
    
    jd = json.loads(res.text)                           
    # print(jd)
    if jd['code'] == 'success':        
        data = {'storename': jd['data']['storename'],   # 存于服务器中的名字
                'url': jd['data']['url'],               # 可直接引用的地址链接
                'hash': jd['data']['hash'],              # 随机字符串，用于删除文件,删除链接为 https://sm.ms/api/delete/hash
                'timestamp': jd['data']['timestamp']    # 上传的时间戳
                } 
        # print(data)
        print('Upload Success.')
    else:
        print(jd['msg'])
    return True

    # requests.post('https://sm.ms/api/upload', files={'smfile': open(img_path, 'rb')})

# 清除上传历史
def clear():        
    url = 'https://sm.ms/api/clear'
    res = requests.get(url)

    jd = json.loads(res.text)                 
    if jd['code'] == 'success':
        print(jd['msg'])
    return True


# 删除某张图
def delete(hash):
    url = 'https://sm.ms/delete/' + hash    
    res = requests.get(url)

    soup = bs(res.text, features ='html.parser')
    a = soup.find_all("div", class_="bs-callout bs-callout-warning")
    print(a[0].string)
    return True

if __name__ == '__main__':
    #history()
    img_path = 'haha.jpg'
    #upload(img_path)
    # clear_all()
    hash = 'RhPKiASxmUloXLCsss'
    delete(hash)

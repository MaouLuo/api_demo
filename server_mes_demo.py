# -*- coding:utf-8 -*-

import requests
import time

# 每分钟相同内容只能发一次，相同内容包括标题和正文
def sever_test():
	url = 'https://sc.ftqq.com/SCU77831Td9cccdfd533462659d8d881e9408da945e1ffad3eb8a8.send'
	data = {
		'text': 'py', # 消息标题，最长为256，必填
        'desp': '1' # 消息内容，最长64Kb，可空，支持MarkDown。
	}
	resp = requests.post(url, data=data)
	print(resp.text)

def main():
    sever_test()


if __name__ == '__main__':
    main()
# utf-8
import json
import re
import time
import random
import config
import urllib.request as request
from selenium import webdriver
import os

# count = 0
# for root, dirs, files in os.walk('./dataJanuary_comment/'):
#     for file in files:
#         with open('./dataJanuary_comment/'+file, 'rb') as fres:
#             for line in fres:
#                 strr = line.decode('utf-8').strip().split(':')
#                 if strr[0] == 'comments':
#                     count = count + 1
# print(count)
# uid = ''
# id = ''
# c = 0
# for root, dirs, files in os.walk('./dataJanuary1/'):
#     for file in files:
#         with open('./dataJanuary1/'+file, 'rb') as fres:
#             for line in fres:
#                 strco = line.decode('utf-8').strip().split(':')
#                 if strco[0] == 'id':
#                     id = str(strco[1])
#                 if strco[0] == 'uid':
#                     uid = str(strco[1])
#                 if strco[0] == 'comments_count':
#                     if (id != '') and (uid != ''):
#                         with open('./data/'+id+'_'+uid, 'ab'):
#                             c = c + 1
# options = webdriver.ChromeOptions()
# options.add_argument(r'--user-data-dir=C:\Users\Laojieduo\AppData\Local\Google\Chrome\User Data1')
# driver = webdriver.Chrome(chrome_options = options)
# driver.get('https://m.weibo.cn/')

def getCookie():
    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=C:\Users\Laojieduo\AppData\Local\Google\Chrome\User Data1')
    driver = webdriver.Chrome(chrome_options = options)
    driver.get('https://m.weibo.cn/')
    cookies = driver.get_cookies()
    cookie_list = []
    for i in cookies:
        cookie = i['name'] + '=' + i['value']
        cookie_list.append(cookie)
    cookie_str = ';'.join(cookie_list)
    print(cookie_str)
    driver.close()
    return cookie_str


def getHtml(url, cookies):
    try:
        print(url)
        opener = request.build_opener()
        opener.addheaders = [('User-Agent', random.choice(headers)), ('cookie', cookies)]
        html = opener.open(url, timeout=10).read()
        text = json.loads(html)
        time.sleep(2)
        return text
    except Exception as e:
        print(e)


headers = config.getheaders()
cookies = getCookie()
json_data = getHtml('https://m.weibo.cn/comments/hotflow?id=4496963279826436&mid=4496963279826436&max_id_type=0', cookies)
for card in json_data['data']['data']:
    try:
        if 'pic' in card:
            pics = [term['url'] for term in card['pic']]
            print(pics)
            # print('pics:' + '****'.join(pics) + '\n')
        created_at = card['created_at']
        time_struct = time.strptime(created_at, '%a %b %d %H:%M:%S +0800 %Y')
        created_at = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
        print(created_at)
    except Exception as e:
        print(e)

# created_at = 'Thu Apr 23 20:15:21 +0800 2020'
# time_struct = time.strptime(created_at, '%a %b %d %H:%M:%S +0800 %Y')
# created_at = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
# print(created_at)
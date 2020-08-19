import json
import re
import time
import random
import config
import urllib.request as request
from selenium import webdriver
import os
from os.path import getsize

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
        time.sleep(60)


def get_comments(filename):
    urll = ''
    post_id = filename.split('_')[0]
    url_original = "http://m.weibo.cn/comments/hotflow?id=" + str(post_id) + '&mid=' + post_id + '&max_id_type=0'
    global count, cooky
    if count >= 300:
        count = 0
        cooky = getCookie()
    max_id, cookies = '', cooky
    with open('./dataJanuary_comment/' + filename, 'ab') as fres:
        for page in range(0, 10):
            if max_id:
                if max_id != '0':
                    url = url_original[:-14] + '&max_id=' + max_id + url_original[-14:]
            else:
                url = url_original
            if url == urll:
                return
            else:
                urll = url
            json_data = getHtml(url, cookies)
            count = count + 1
            if not json_data: continue
            if json_data['ok'] == 0: return
            max_id = str(json_data['data']['max_id'])
            for card in json_data['data']['data']:
                fres.write(('comments:' + re.sub('<[^<]+?>', '', card['text']) + '\n').encode('utf-8'))
                fres.write(('like_count:' + str(card['like_count']) + '\n').encode('utf-8'))
                fres.write(('user_name:' + card['user']['screen_name'] + '\n').encode('utf-8'))
                fres.write(('user_id:' + str(card['user']['id']) + '\n\n').encode('utf-8'))
                fres.flush()


if __name__ == "__main__":
    str_id, str_uid = '', ''
    count = 0
    cooky = getCookie()
    headers = config.getheaders()
    post_id_to_get, post_id_get = [], set()
    for root, dirs, files in os.walk('./dataJanuary_comment/'):
        for file in files:
            if float(getsize('D:\\Desktop\\GetComments\\dataJanuary_comment\\'+file))/float(1024) == 0:
                get_comments(file)

import json
import re
import time
import random
import config
import urllib.request as request
from selenium import webdriver
import os

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
    if filename in post_id_get: return
    post_id_get.add(filename)
    with open('./post_id_comment_get', 'ab') as comm:
        comm.write((filename+'\n').encode('utf-8'))
    post_id = filename.split('_')[0]
    url_original = "http://m.weibo.cn/comments/hotflow?id=" + str(post_id) + '&mid=' + str(post_id) + '&max_id_type=0'
    global count, cooky
    if count >= 300:
        count = 0
        cooky = getCookie()
    max_id, cookies = '', cooky
    with open('./dataJanuary_comment11/' + filename, 'wb') as fres:
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
                try:
                    if 'pic' in card:
                        fres.write(('pic:'+str(card['pic']['url'])+'\n').encode('utf-8'))
                    created_at = card['created_at']
                    time_struct = time.strptime(created_at, '%a %b %d %H:%M:%S +0800 %Y')
                    created_at = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
                    fres.write(('created_at:'+str(created_at)+'\n').encode('utf-8'))
                except Exception as e:
                    print(e)
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
    with open('./post_id_comment_get', 'rb') as comm:
        for line in comm:
            post_id_get.add(line.decode('utf-8').strip())
    for root, dirs, files in os.walk('./dataJanuary11/'):
        for file in files:
            with open('./dataJanuary11/'+file, 'rb') as fress:
                for lines in fress:
                    a = lines.decode('utf-8').strip().split(':')
                    if a[0] == 'id':
                        str_id = str(a[1])
                    if a[0] == 'uid':
                        str_uid = str(a[1])
                    if a[0] == 'comments_count':
                        if int(a[1]) > 0:
                            strr = str_id + '_' + str_uid
                            get_comments(strr)


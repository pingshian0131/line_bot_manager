import requests
import time
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json
import sys


PTT_URL = 'https://www.ptt.cc'
count = 0
article_num = 0

def get_web_page(url):
    global count
    count += 1
    print (count)
    time.sleep(0.5)  # 每次爬取前暫停 0.5 秒以免被 PTT 網站判定為大量惡意爬取
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    print (url)
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_articles(dom, board_name , push_num , search_title):
    global PTT_URL , article_num 
    soup = BeautifulSoup(dom, 'html.parser')
#    print (soup)
#    f_path = '/Users/pingshian/Desktop/Gossiping.txt'
#    with open (f_path , 'w' , encoding = 'utf-8') as f:
#        f.write (str(soup))
#    input ()
#    sys.exit ()
    # 取得上一頁的連結

    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']
    
    articles = []  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        Y , M , D = time.strftime("%Y %m %d").split()
        date = Y + '/' + d.find('div', 'date').string.strip()  # 發文日期 
            # 取得推文數
        push_count = 0
        if d.find('div', 'nrec').string:
            try:
                if d.find('div', 'nrec').string == '爆': push_count = 100
                push_count = int(d.find('div', 'nrec').string)  # 轉換字串為數字
            except ValueError:  # 若轉換失敗，不做任何事，push_count 保持為 0
                pass
        if push_num == "":
            if search_title != None:
                if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                    if re.search (search_title , d.find ('a').string , re.IGNORECASE) != None:
                        href = PTT_URL + d.find('a')['href']
                        title = d.find('a').string
                        article_num += 1
                        articles.append({
                            'Id':article_num ,
                            'board_name':board_name ,
                            'title': title ,
                            'url': href ,
                            'date': date , 
                            'search':search_title ,
                            'push_count': push_count ,
                            'push_num': None 
                        })
            else:
                if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                    href = PTT_URL + d.find('a')['href']
                    title = d.find('a').string
                    article_num += 1
                    articles.append({
                        'Id':article_num ,
                        'board_name':board_name ,
                        'title': title ,
                        'url': href ,
                        'date': date , 
                        'search':search_title ,
                        'push_count': push_count ,
                        'push_num': None  
                    })
        elif push_num != "":
            if push_count > int (push_num): 
                if search_title == None:
                    if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                        href = PTT_URL + d.find('a')['href']
                        title = d.find('a').string
                        article_num += 1
                        articles.append({
                            'Id':article_num ,
                            'board_name':board_name ,
                            'title': title ,
                            'url': href ,
                            'date': date ,
                            'search':search_title ,
                            'push_count': push_count ,
                            'push_num': push_num
                        })
                else:
                    if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                        if re.search (search_title , d.find ('a').string , re.IGNORECASE) != None:
                            href = PTT_URL + d.find('a')['href']
                            title = d.find('a').string
                            article_num += 1
                            articles.append({
                                'Id':article_num ,
                                'board_name':board_name ,
                                'title': title ,
                                'url': href ,
                                'date': date ,
                                'search':search_title ,
                                'push_count': push_count ,
                                'push_num': push_num
                            })

    return articles, prev_url  


def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    links = soup.find(id='main-content').find_all('a')
    img_urls = []
    for link in links:
        if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            img_urls.append(link['href'])
    return img_urls


def save(img_urls, title):
    if img_urls:
        try:
            dname = title.strip()  # 用 strip() 去除字串前後的空白
            os.makedirs(dname)
            for img_url in img_urls:
                if img_url.split('//')[1].startswith('m.'):
                    img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'
                fname = img_url.split('/')[-1]
                urllib.request.urlretrieve(img_url, os.path.join(dname, fname))
        except Exception as e:
            print(e)

def main (board_name , push_num , search_title):
    global count , article_num 
    current_page = get_web_page(PTT_URL + '/bbs/' + board_name + '/index.html')
#    current_page = get_web_page(PTT_URL + '/bbs/Beauty/index.html')
    if current_page:
        articles = []  # 全部的今日文章
        date = time.strftime("%m/%d").lstrip('0')  # 今天日期, 去掉開頭的 '0' 以符合 PTT 網站格式
        current_articles, prev_url = get_articles(current_page, board_name , push_num , search_title)  # 目前頁面的今日文章
        if push_num == "":
            article_target = 31
        else:
            article_target = 12
        while article_num < article_target:  # 若目前頁面有今日文章則加入 articles，並回到上一頁繼續尋找是否有今日文章
            print ("article_num: {}".format (article_num))
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, board_name , push_num , search_title)

        # 已取得文章列表，開始進入各文章讀圖
        print ("已取得文章共：" , len (articles) , "篇")
#        for article in articles:
#            print('Processing', article)
#            page = get_web_page(PTT_URL + article['href'])
#            if page:
#                img_urls = parse(page)
#                save(img_urls, article['title'])
#                article['num_image'] = len(img_urls)

        # 儲存文章資訊
#        with open('data.json', 'w', encoding='utf-8') as f:
#            json.dump(articles, f, indent=2, sort_keys=True, ensure_ascii=False)
        count = 0
        article_num = 0
#        return json.dump(articles, f, indent=2, sort_keys=True, ensure_ascii=False)
        return articles


import requests
import json
import re
import csv
import time
from urllib.parse import urlencode
from lxml import etree

CNT = 0
MAX_PAGE = 1000
base_url = 'https://api.bilibili.com/x/web-interface/web/channel/multiple/list?'
start_url = 'https://api.bilibili.com/x/web-interface/web/channel/multiple/list?channel_id=530918&sort_type=new&page_size=30'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    'Origin': 'https://www.bilibili.com'
}


def get_and_parse_cookies(error):
    if error:
        response = requests.get('http://localhost:5555/bilibili/random')
        jar = requests.cookies.RequestsCookieJar()
        cookies = response.text
        if type(cookies) == str:
            cookies = eval(cookies)
            for cookie in cookies:
                jar.set(cookie['name'], cookie['value'])
            return jar
        elif type(cookies) == bytes:
            cookies = eval(cookies.decode())
            for cookie in cookies:
                jar.set(cookie['name'], cookie['value'])
            return jar
        else:
            return


def get_proxy(error):
    if error:
        response = requests.get('http://localhost:5000/random')
        proxy = response.text
        print(proxy)
        proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy,
                }
        return proxies        


def re_search_digit(text):
    patton = re.compile('\d+')
    ret = re.search(patton, text)
    if not ret:
        return 0
    return ret


def get_next_page_url(offset):
    params = {
        'channel_id': '530918',
        'sort_type': 'new',
        'offset': offset,
        'page': '30'
    }
    return base_url + urlencode(params)


def get_video_url(bvid):
    return 'https://www.bilibili.com/video/' + bvid


def crawl_video_time(bvid, cookies, proxies):
    video_url = get_video_url(bvid)
    response = requests.get(video_url, headers=headers, cookies=cookies, proxies=proxies)
    response.encoding = 'utf-8'
    html = etree.HTML(str(response.text))
    video_date = html.xpath('//*[@id="viewbox_report"]/div[1]/span[2]/text()')[0]
    return video_date

def crawl_video_info(bvid, cookies, proxies):
    # bvid获取cid
    print('step into function: crawl_video_info()...')
    cid_url = 'https://api.bilibili.com/x/player/pagelist?bvid=' + bvid
    try:
        cid_res = requests.get(cid_url, headers=headers, cookies=cookies, proxies=proxies)
        cid_data = cid_res.json()
        cid = cid_data.get("data")[0].get("cid")
        params = {
            'cid': cid,
            'bvid': bvid
        }
        aid_base_url = 'https://api.bilibili.com/x/web-interface/view?'
        aid_url = aid_base_url + urlencode(params)
        aid_res = requests.get(aid_url, headers=headers, cookies=cookies, proxies=proxies)
        aid_data = aid_res.json()
        video_info = aid_data.get("data").get("stat")
        aid = video_info.get("aid")
        view = video_info.get("view")
        danmaku = video_info.get("danmaku")
        like = video_info.get("like")
        coin = video_info.get("coin")
        collect = video_info.get("favorite")
    except:
        print('IP 被禁了....{}'.format(aid_res.status_code))
        new_jar = get_and_parse_cookies(True)
        proxies = get_proxy(True)
        return crawl_video_info(bvid, new_jar, proxies)
    return view, danmaku, like, coin, collect


def crawl_page(url, cookies, proxies):
    print('step into function: craw_page()...')
    r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies)
    r.encoding = 'utf-8'
    json_info = r.json()
    data = json_info.get('data')
    offset = data.get('offset')
    list_info = data.get('list')
    for video in list_info:
        cover =video.get('cover')
        duration = video.get('duration')
        bvid = video.get('bvid')
        # video_date = crawl_video_time(bvid, jar, proxies)
        view, danmaku, like, coin, collect = crawl_video_info(bvid, jar, proxies)
        # print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t'.format(cover, duration, bvid, view, danmaku, like, coin, collect))
        global CNT
        CNT = CNT+1
        print('正在写入第{}个视频....'.format(CNT))
        writer.writerow([cover, duration, bvid, view, danmaku, like, coin, collect])
        # if CNT %100 == 0:
        #     time.sleep(360)
    return offset




if __name__ == '__main__':
    start = time.time()
    file = open('info_{}.csv'.format(MAX_PAGE), 'w')
    writer = csv.writer(file)
    writer.writerow(['cover', 'duration', 'bvid', 'view', 'danmaku', 'like', 'coin', 'collect'])
    jar = get_and_parse_cookies(True)
    proxies = get_proxy(True)
    for page in range(0, MAX_PAGE):
        if page == 0:
            offset = crawl_page(start_url, jar, proxies)
        else:
            url = get_next_page_url(offset)
            offset = crawl_page(url, jar, proxies)
    file.close()
    end = time.time()
    print('总共耗时{:.2}min'.format((end-start)/60))

import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
from redis import StrictRedis
from urllib.parse import quote, urlencode, unquote


REDIS_NAME = 'ValuedVideos4'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''


start_url = 'https://www.bilibili.com/video/'


class Crawl():
    def __init__(self, start_bv, name = REDIS_NAME, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
            'Origin': 'https://www.bilibili.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        self.db = StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.bv = []
        self.bv.append(start_bv)
        self.status = True
        self.start_url = start_url
        self.count = 0
        self.name = name

    def get_proxy(self):
        r = requests.get("http://localhost:5000/random")
        proxy = r.text
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        return proxies


    def get_cookies(self):
        """
        get the cookies from cookies pool
        :return: cookies(RequestsCookieJar)
        """
        cookies = requests.get('http://localhost:5555/bilibili/random')
        jar = requests.cookies.RequestsCookieJar()
        cookies = cookies.text
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
            return False


    def download_img(self, mid, name):
        print(name)
        proxies = self.get_proxy()
        cookies = self.get_cookies()
        quote_name = quote(name)
        base_url = 'https://api.bilibili.com/x/space/arc/search?'
        params = {
            'mid': mid,
            'ps': '30',
            'tid': '0',
            'pn': '1',
            'keyword': name,
            'order': 'pubdata',
            'jsonp': 'jsonp'
        }
        api_url = base_url + urlencode(params)
        print(api_url)
        try:
            response = requests.get(api_url, headers=self.headers, cookies=cookies, proxies=proxies, timeout=10)
            json = response.json()
            print(json)
            img_url = 'https:' + json.get("data").get("list").get("vlist")[0].get("pic")
            img = requests.get(img_url, headers=self.headers, proxies=proxies, cookies=cookies)
            len_bv = len(self.bv)
            print('正在获取图片')
            with open('./cover/{}.jpg'.format(self.bv[len_bv-1]), 'wb') as f:
                f.write(img.content)
        except:
            return

    def storage_info(self, video_html):
        """
        download the cover and storage the BV of the video
        :return: BV
        """

        a = video_html.find(name='a')
        href = a.attrs['href']
        bv = re.search(r'/(BV\w+)/', href).group(1)
        if self.if_have_crawled(bv):
           return
        href = video_html.find(attrs={'target': '_blank'}).attrs['href']
        mid = re.search('\/(\d+)\/', href).group(1)
        title = video_html.find(attrs={'class': 'title'})
        name = title.attrs['title']
        print("正在获取：标题为\t{}\t，BV号\t{}\t为的信息".format(name, bv))
        self.db.sadd(self.name, bv)
        self.bv.append(bv)
        self.download_img(mid, name)


    def if_have_crawled(self, new_bv):
        return self.db.sismember(self.name, new_bv)


    def crawl_page_and_info(self):
        """
        to find the recommended videos list, parse it, and find the target video BV
        :return: True or False, tell that if there are no new videos to crawl
        """
        url = self.start_url + self.bv.pop(0)
        self.count = 0
        cookies = self.get_cookies()

        try:
            res = requests.get(url, headers=self.headers, cookies=cookies, timeout=10)
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, 'lxml')
            rec_list = soup.find_all(attrs={'class': 'video-page-card'})
            for rec_video in rec_list:
                data_tag = rec_video.find(lambda tag: tag.get('class') == ['count'])
                data = data_tag.string
                r = re.search('(\d+\.?\d*).*?(\d+\.?\d*)', data)
                view, danmu = r.groups()
                if view == '0' and danmu != '0':
                    self.storage_info(rec_video)
        except:
            return




    def test_cookies(self):
        """
        to test if the cookies is valid
        :return: True or False
        """
        pass


    def main(self):
        while len(self.bv):
            self.crawl_page_and_info()
            print(len(self.bv))



if __name__ == '__main__':
    c = Crawl('BV16f4y1276T')
    c.main()


import requests
from redis import StrictRedis
import re
from bs4 import BeautifulSoup
from urllib.parse import urlencode

REDIS_NAME = 'ValuedVideos3'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''

start_url = 'https://www.bilibili.com/video/'

class DLBiliimg():
    def __init__(self, mid=None, name=None, start_url=start_url):
        self.mid = mid
        self.name = name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
            'Origin': 'https://www.bilibili.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }
        self.start_url = start_url

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

    def get_proxy(self):
        """
        get proxy
        :return: proxy
        """
        r = requests.get("http://localhost:5000/random")
        proxy = r.text
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        return proxies

    def without_mid_and_name(self, cookies, bv):
        """
        get mid and name for function:with_mid_and_name
        :param cookies: cookies
        :param bv: the bv of the target video
        :return: none
        """
        try:
            url = self.start_url + bv
            response = requests.get(url, headers=self.headers, cookies=cookies, timeout=5)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, 'lxml')
            title = soup.find(name='span', attrs={'class': 'tit'})
            name = title.string
            link = soup.find(attrs={'report-id': 'head'})
            href = link.attrs['href']
            mid = re.search('\/(\d+)', href).group(1)
            self.with_mid_and_name(cookies, bv=bv, mid=mid, name=name)
        except:
            return



    def with_mid_and_name(self, cookies, bv, mid, name):
        """
        download image
        :param cookies:
        :param bv:
        :param mid:
        :param name:
        :return:
        """
        print(name)
        proxies = self.get_proxy()
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
        try:
            response = requests.get(api_url, headers=self.headers, cookies=cookies, proxies=proxies, timeout=10)
            json = response.json()
            print(json)
            img_url = 'https:' + json.get("data").get("list").get("vlist")[0].get("pic")
            print(img_url)
            with open('img_url.txt', 'a+') as f:
                f.write('\n')
                f.write(img_url)
            print("preparing")
            img = requests.get(img_url, headers=self.headers, cookies=cookies, proxies=proxies, timeout=10)
            print('正在获取图片')
            with open('./cover/{}&{}.jpg'.format(bv, name), 'wb') as f:
                f.write(img.content)
        except:
            return

if __name__ == '__main__':
    db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    bv_iter = db.sscan_iter(REDIS_NAME)

    dl_img = DLBiliimg()
    for bv in bv_iter:
        cookies = dl_img.get_cookies()
        dl_img.without_mid_and_name(cookies, bv)
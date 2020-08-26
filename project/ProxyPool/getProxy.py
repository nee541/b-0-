import json
from lxml import etree
import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.135 Safari/537.36'
}

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        proxy = eval("self.{}()".format(callback))
        proxies = list(set(proxies + proxy))
        return proxies

    def crawl_kuaidaili(self):
        start_url = 'https://www.kuaidaili.com/free/'
        try:
            r = requests.get(start_url, headers=HEADERS, timeout=3)
        except:
            print('error')
            self.crawl_kuaidaili()
        html = etree.HTML(r.text)
        res = int(html.xpath('//*[@id="listnav"]/ul/li/a/text()')[-1])
        proxy = []
        for page in range(1, 10):
            try:
                if page != 1:
                    url = start_url + 'inha/' + str(page) + '/'
                    r = requests.get(url, headers=HEADERS, timeout=3)
                    html = etree.HTML(r.text)
            except:
                continue
            docs = html.xpath('//*[@id="list"]/table/tbody/tr')
            for doc in docs:
                ip = doc.xpath('td[@data-title="IP"]/text()')[0]
                port = doc.xpath('td[@data-title="PORT"]/text()')[0]
                proxy.append(ip + port)
            print(proxy)
        return proxy


    def crawl_66ip(self):
        formate = 'gb2312'
        start_url = 'http://www.66ip.cn/'
        r = requests.get(start_url, headers=HEADERS)
        r.encoding = formate
        html = etree.HTML(r.text)
        res = int(html.xpath('//*[@id="PageList"]/a/text()')[-2])
        print(res)
        proxy = []
        for page in range(1, res+1):
            print(page)
            if page != 1:
                try:
                    url = start_url + str(page) + '.html'
                    r = requests.get(url, headers=HEADERS)
                    r.encoding = 'gb2312'
                    html = etree.HTML(r.text)
                except:
                    continue
            docs = html.xpath('//*[@id="main"]/div/div[1]/table/tr')[1:]
            for doc in docs:
                ip = doc.xpath('td[1]/text()')[0]
                port = doc.xpath('td[2]/text()')[0]
                proxy.append(ip + ':' + port)
        return proxy

    def crawl_ip3366(self):
        start_url = 'http://www.ip3366.net/free/'
        r = requests.get(start_url, headers=HEADERS)
        encoding_format = requests.utils.get_encodings_from_content(r.text)[0]
        r.encoding = encoding_format
        html = etree.HTML(r.text)
        res = int(html.xpath('//*[@id="listnav"]/ul/a/text()')[-3])
        proxy = []
        for page in range(1, res):
            print(page)
            params = {
                'stype': '1',
                'page': page
            }
            if page != 1:
                url = start_url + '?' + urlencode(params)
                r = requests.get(url, headers=HEADERS)
                r.encoding = encoding_format
                html = etree.HTML(r.text)
            docs = html.xpath('//*[@id="list"]/table/tbody/tr')
            for doc in docs:
                ip = doc.xpath('./td[1]/text()')[0]
                port = doc.xpath('./td[2]/text()')[0]
                proxy.append(ip + ':' + port)
        return proxy

    def crawl_xiladaili(self):
        start_url = 'http://www.xiladaili.com/https/'
        r= requests.get(start_url, headers=HEADERS)
        encoding_format = requests.utils.get_encodings_from_content(r.text)
        r.encoding = encoding_format
        html = etree.HTML((r.text))
        res = 1000
        proxy = []
        for page in range(1, res):
            print(page)
            if page != 1:
                url = start_url + str(page) + '/'
                r = requests.get(url, headers=HEADERS)
                r.encoding = encoding_format
                html = etree.HTML(r.text)
            docs = html.xpath('/html/body/div/div[3]/div[2]/table/tbody/tr')
            for doc in docs:
                proxy_res = doc.xpath('./td[1]/text()')[0]
                proxy.append(proxy_res)
        return proxy


    def crawl_xdaili(self):
        url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=c3d3ad12c8cf4cdfb8922830117189ba&orderno=YZ20208261473nzIwPu&returnType=2&count=10'
        response = requests.get(url)
        json = response.json()
        result = json.get("RESULT")
        proxies = []
        for r in result:
            ip = r.get("ip")
            port = r.get("port")
            proxy = ip + ':' + port
            proxies.append(proxy)
        return proxies

from storage import RedisClient


if __name__ == '__main__':
    c = Crawler()
    proxies = c.get_proxies('crawl_xiladaili')
    print(proxies)
    print(len(proxies))

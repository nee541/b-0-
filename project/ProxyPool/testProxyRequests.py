import requests
import time
from redis import StrictRedis
from storage import RedisClient

url = 'https://api.bilibili.com/x/space/arc/search?mid=5309294&ps=30&tid=0&pn=1&keyword=%E3%80%90MMD%E3%80%91Number9+%28Luka+%26+Isuzu%29&order=pubdata&jsonp=jsonp'

class Tester():
    def __init__(self, test_url=url):
        self.test_url = test_url
        self.db = RedisClient()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
            'Origin': 'https://www.bilibili.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
        }

    def test_single_proxy(self, proxy):
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        try:
            response = requests.get(self.test_url, headers=self.headers, proxies=proxies, timeout=5)
            json = response.json()
            code = json.get('data')
            if code != None:
                self.db.max(proxy)
                print(' 代理可用 ', proxy)
            else:
                print(' 请求响应码不合法, 不可用 ', proxy)
                self.db.decrease(proxy)
        except:
            print(' 代理请求失败 ', proxy)
            self.db.decrease(proxy)

    def run(self):
        print(' 测试器开始运行 ')
        proxies = self.db.all()
        for proxy in proxies:
            print(' 正在测试 ', proxy)
            self.test_single_proxy(proxy)

if __name__ == '__main__':
    t = Tester()
    t.run()
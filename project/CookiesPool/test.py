from storage import RedisClient

retry_count = 0

TEST_URL_MAP = {
        'bilibili': 'https://api.bilibili.com/x/web-interface/nav'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    'Origin': 'https://www.bilibili.com'
}


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.item():
            self.test(username, cookies)


def retry(username, cookies):
    retry_info = BilibiliValidTester()
    retry_info.test(username, cookies)



import json
import requests
from requests.exceptions import ConnectionError

class BilibiliValidTester(ValidTester):
    def __init__(self, website='bilibili'):
        ValidTester.__init__(self, website)

    def test(self, username, cookies):
        global retry_count
        print('Testing cookies {} ...'.format(username))
        try:
            if type(cookies) == str:
                cookies = eval(cookies)
            else:
                cookies = eval(cookies.decode())
        except TypeError:
            print('Cookies Error: {} !'.format(username))
            self.cookies_db.delete(username)
            print('Have deleted Cookies: {}'.format(username))
            return
        try:
            jar = requests.cookies.RequestsCookieJar()
            for cookie in cookies:
                jar.set(cookie['name'], cookie['value'])
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url, headers=headers, cookies=jar, timeout=5, allow_redirects=False)
            isLogin = response.json().get("data").get("isLogin")
            if isLogin:
                print('用户名:{}'.format(response.json().get("data").get("uname")))
                print('Valid Cookies')
                retry_count = 0
            else :
                print(response.status_code, response.headers)
                print('Invalid Cookies: {}'.format(username))
                self.cookies_db.delete(username)
                print('Delete Cookies: {}'.format(username))
        except ConnectionError as e:
            retry_count = retry_count + 1
            print('发生异常', e.args)
            if retry_count <= 5:
                print('第{}次重试...'.format(retry_count))
                retry(username, cookies)
            else:
                print('网络错误')
                return

    def run(self):
        cookies_usernames = self.cookies_db.all_keys()
        for username in cookies_usernames:
            cookies = self.cookies_db.get(username)
#             print(cookies)
            self.test(username, cookies)


if __name__ == '__main__':
    test_cookie = BilibiliValidTester()
    test_cookie.run()

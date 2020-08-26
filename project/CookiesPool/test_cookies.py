import requests
from redis import StrictRedis
import json
import demjson

TEST_URL = 'https://api.bilibili.com/x/web-interface/nav'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    'Origin': 'https://www.bilibili.com'
}
cookies_db = StrictRedis('localhost', 6379)
cookies = cookies_db.hget('cookies:bilibili', '19801298267')
# print(cookies)
cookies = cookies.decode()
cookies = eval(cookies)

c = requests.cookies.RequestsCookieJar()
for cookie in cookies:
    c.set(cookie['name'], cookie['value'])
print(c)
response = requests.get(TEST_URL, headers=headers)
data = response.json()
# print(response.text)
isLogin = data.get("data").get("isLogin")
print(data)
print(isLogin)


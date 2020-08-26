import json
from flask import Flask, g
from storage import*

API_HOST = 'localhost'
API_PORT = '5555'

app = Flask(__name__)
# 生成模块的配置字典
GENERATOR_MAP = {'weibo': 'WeiboCookiesGenerator', 'bilibili': 'BilibiliCookiesGenerator'}
@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'

def get_conn():
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
    return g

@app.route('/<website>/random')
def get_random_cookie(website):
    """
    获取随机的 Cookie, 访问地址如 /weibo/random
    :return: 随机 Cookie
    """
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, debug=True)

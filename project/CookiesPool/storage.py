import random
from redis import StrictRedis

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = ''

class RedisClient(object):
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = StrictRedis(host, port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        return self.db.hget(self.name(), username)

    def delete(self, username):
        return self.db.hdel(self.name(), username)

    def count(self):
        return self.db.hlen(self.name())

    def random(self):
        return random.choice(self.db.hvals(self.name()))

    def username(self):
        return self.db.hkeys(self.name())

    def all(self):
        return self.db.hgetall(self.name())

    def all_keys(self):
        return self.db.hkeys(self.name())

if __name__ == '__main__':
    accounts = RedisClient('accounts', 'bilibili')
    print('请输入账号个数：')
    num = int(input())
    for i in range(0, num):
        username = input('请输入账号:')
        password = input('请输入密码:')
        accounts.set(username, password)

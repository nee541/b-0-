from storage import RedisClient
from getProxy import Crawler

POOL_UPPER_THRESHOLD = 10000


class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """判断是否达到了代理池限制"""
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run_all(self):
        print(' 获取器开始执行 ')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)

    def run_specific(self, callback):
        print(' 获取器开始执行 ')
        if not self.is_over_threshold():
            proxies = self.crawler.get_proxies(callback)
            for proxy in proxies:
                self.redis.add(proxy)


if __name__ == '__main__':
    g = Getter()
    g.run_specific('crawl_xdaili')
TESTER_CYCLE = 10
GETTER_CYCLE = 300
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

from multiprocessing import Process
from API import app
from RunGetProxy import Getter
from testProxyRequests import Tester
from storage import RedisClient
import time


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """定时测试代理"""
        tester = Tester()
        while True:
            print(' 测试器开始运行 ')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """定时获取代理"""
        getter = Getter()
        db = RedisClient()
        while True:
            print(' 开始抓取代理 ')
            getter.run_specific('crawl_xdaili')
            db.clear()
            time.sleep(cycle)

    def schedule_api(self):
        """开启 API"""
        app.run()

    def run(self):
        print(' 代理池开始运行 ')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__ == '__main__':
    s = Scheduler()
    s.run()
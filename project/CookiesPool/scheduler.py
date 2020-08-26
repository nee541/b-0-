import time
from multiprocessing import Process
from api import app
from generate import*
from test import*

TESTER_MAP = {'bilibili': 'BilibiliValidTester'}
GENERATOR_MAP = {'bilibili': 'BilibiliCookieGenerator'}
API_HOST = 'localhost'
API_PORT = '5555'

CYCLE = 180
# 产生模块开关
GENERATOR_PROCESS = True
# 验证模块开关
VALID_PROCESS = True
# 接口模块开关
API_PROCESS = True

class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while GENERATOR_PROCESS:
            print('Cookies 检测进程开始运行 ')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('Cookies 检测完成 ')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while VALID_PROCESS:
            print('Cookies 生成进程开始运行 ')
            try:
                for website, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('Cookies 生成完成 ')
#                     generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('API 接口开始运行 ')
        app.run(host=API_HOST, port=API_PORT, debug=True)

    def run_process(self):
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()

if __name__ == '__main__':
    Scheduler().run_process()

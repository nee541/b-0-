import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

URL = 'https://passport.bilibili.com/login'
# USERNAME = '19801298267'
# PASSWORD = 'Kywyaas@16'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

class BilibiliCookies():
    def __init__(self, USERNAME, PASSWORD):
        self.url = URL
        self.username = USERNAME
        self.password = PASSWORD
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1366, 768)
        self.wait = WebDriverWait(self.browser, 10)

    def login(self):
        self.browser.get(self.url)

        username = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-username"]')))
        password = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-passwd"]')))
        submit = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="geetest-wrap"]/div/div[5]/a[1]')))

        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def captcha(self):
        print('请手动完成验证过程，限时20s....')
        time.sleep(20)
        print('时间到')
   
    def new_page(self):
        try:
            homepage = self.browser.find_element_by_xpath('//*[@id="internationalHeader"]/div[1]/div/div[3]/div[2]/div[1]/span/div/img')
            return {'value': 1, 'content': 'OK'}
        except NoSuchElementException:
            return {'value': 0, 'content': 'ERROR!'}

    def cookie(self):
        self.login()
        self.captcha()
        res = self.new_page()
        if res['value'] == 1:
            print(res['content'])
            cookies = self.browser.get_cookies()
            self.browser.close()
            return cookies
        else :
            print('Please try again')
            return ''
        
from storage import RedisClient
class BilibiliCookieGenerator(object):
    def __init__(self, website):
        self.website = website

    def run(self):
        accounts = RedisClient('accounts', self.website)
        cookies = RedisClient('cookies', self.website)
        accounts_usernames = accounts.all_keys()
        cookies_usernames = cookies.all_keys()
        for username in accounts_usernames:
            if username not in cookies_usernames:
                password = accounts.get(username)
                print('正在生成Cookies, 账号:{} 密码: {}'.format(username, password))
                new = BilibiliCookies(username, password)
                new_cookies = new.cookie()
                if new_cookies:
                    print('生成Cookies成功')
                else :
                    print('生成Cookies失败')
                cookies.set(username, new_cookies)


if __name__ == '__main__':
    bili = BilibiliCookies(USERNAME='19801298267', PASSWORD='Kywyaas@16')
    print(bili.cookie())



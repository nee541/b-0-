# import requests
# from lxml import etree
#
# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   'Chrome/84.0.4147.135 Safari/537.36'
#     # 'Host': 'www.kuaidaili.com'
# }
#
# # start_url = 'https://www.kuaidaili.com/free/'
# # r = requests.get(start_url, headers=HEADERS)
# # html = etree.HTML(r.text)
# # res = html.xpath('//*[@id="listnav"]/ul/li/a/text()')
# # print(type(int(res[-1])))
# # proxy = []
# # docs = html.xpath('//*[@id="list"]/table/tbody/tr')
# # for doc in docs:
# #     print(doc)
# #     ip = doc.xpath('td[@data-title="IP"]/text()')[0]
# #     port = doc.xpath('td[@data-title="PORT"]/text()')[0]
# #     proxy.append(ip + port)
# # print(type(ip))
# # print(proxy)
#
# decoding = 'gb2312'
# start_url = 'http://www.66ip.cn/'
# r = requests.get(start_url, headers=HEADERS)
# # print(r.encoding)
# html = etree.HTML(r.text)
# # print(r.text)
# # print(requests.utils.get_encodings_from_content(r.text))
# r.encoding = 'gb2312'
# # print(r.text)
# res = int(html.xpath('//*[@id="PageList"]/a/text()')[-2])
# print(res)
# proxy = []
# for page in range(0, 10):
#     print(page)
#     if page != 0:
#         url = start_url + str(page) + '.html'
#         r = requests.get(url, headers=HEADERS)
#         r.encoding = 'gb2312'
#         html = etree.HTML(r.text)
#     # print(etree.tostring(html).decode('utf-8'))
#     docs = html.xpath('//*[@id="main"]/div/div[1]/table/tr')[1:]
#     test = html.xpath('//*[@id="main"]/div/div[1]/table/tr')
#     # print(test)
#     # print(etree.tostring(test[0]).decode(decoding))
#     for doc in docs:
#         ip = doc.xpath('td[1]/text()')[0]
#         port = doc.xpath('td[2]/text()')[0]
#         proxy.append(ip + ':' + port)
#         print(ip + ':' + port)

import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '\
                  'Chrome/84.0.4147.135 Safari/537.36'
    # 'Host': 'www.kuaidaili.com'
}

r = requests.get('http://localhost:5000')
proxy = '103.206.253.82:8080'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

response = requests.get('https://www.bilibili.com/' ,headers=HEADERS, proxies=proxies)
print(response.status_code)

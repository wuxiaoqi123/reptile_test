# coding=utf-8

'''
爬取小说
'''

__author__ = 'wuxiaoqi'

import requests
# from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
}

URL = 'https://www.biqukan.com'
NAME = "一念永恒"


def saveTxt(text):
    with open(NAME, 'a', encoding='utf-8') as f:
        f.write(text)


def parseCatalog(url_address):
    '''
    解析目录
    '''
    url_address = URL + url_address
    response = requests.get(url=url_address, headers=headers)
    if response.status_code == 200:
        html = response.text
        doc = pq(html)
        catalog = False
        for item in doc('div.listmain dd a').items():
            if '章节目录' == item.text():
                catalog = True
            if catalog:
                yield (item.text(), URL + item.attr('href'))


def parseContent(action):
    '''
    解析正文
    '''
    url = action[1]
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        doc = pq(response.text)
        try:
            saveTxt(doc('div.showtxt').text().split()[0])
            print('完成:' + action[0])
        except Exception as e:
            print('出错:' + action[0])


if __name__ == '__main__':
    for action in parseCatalog('/1_1094/'):
        parseContent(action)

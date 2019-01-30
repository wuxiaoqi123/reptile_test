# coding=utf-8
import requests
from pyquery import PyQuery as pq
import os

url = 'http://www.budejie.com/'

headers = {
    'User-Agent': 'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36'
}


def get_page(page):
    '''
    获取指定页数的数据
    :param page:  要获取的页数据
    :return: 网页内容
    '''
    page_url = url + str(page)
    try:
        response = requests.get(page_url, headers=headers)
        return response.content.decode('utf-8')
    except requests.ConnectionError as e:
        print("Error request:", e.args)


def parse_page(html):
    '''
    解析网页数据
    :param html:
    :return:
    '''
    doc = pq(html)
    items = doc('.lazy').items()
    for item in items:
        yield {'title': item.attr('alt'),
               'img': item.attr('data-original')}


def download(filename, img_url):
    path = 'budejie'
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    split = img_url.split('.')
    if split[-1] == 'jpg' or split[-1] == 'gif':
        filename = filename.strip().replace('\n', '') + '.' + split[-1]
        response = requests.get(img_url)
        with open(path + "/" + filename, 'wb') as f:
            f.write(response.content)


if __name__ == '__main__':
    html = get_page(1)
    data = parse_page(html)
    for d in data:
        download(d['title'], d['img'])

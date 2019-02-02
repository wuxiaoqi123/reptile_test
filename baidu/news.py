# coding=utf-8
import requests
import time
import pymongo

# http://news.baidu.com/widget?id=LocalNews&ajax=json&t=1549093699049
URL = 'http://news.baidu.com/widget?id=LocalNews&ajax=json&t='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def index_page():
    '''
    获取数据
    '''
    url = URL + str(int(time.time()))
    response = requests.get(url, headers=headers)
    return response.json()


def parse_json(objjson):
    '''
    解析数据
    :param objjson: json对象
    '''
    try:
        rows = objjson['data']['LocalNews']['data']['rows']
        for row in rows['first']:
            yield {
                'imgUrl': row['imgUrl'],
                'time': row['time'],
                'title': row['title'],
                'url': row['url']
            }
        for row in rows['second']:
            yield {
                'imgUrl': row['imgUrl'],
                'time': row['time'],
                'title': row['title'],
                'url': row['url']
            }
    except:
        print('解析异常')


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'baidu_news'
MONGO_COLLECTION = 'news'
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
db_collection = db[MONGO_COLLECTION]


def save_data(data):
    try:
        if db_collection.insert_one(data):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


if __name__ == '__main__':
    page = index_page()
    datas = parse_json(page)
    for data in datas:
        save_data(data)

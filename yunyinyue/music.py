# coding=utf-8
import json

import pymongo
import requests
from pyquery import PyQuery as pq
from requests.exceptions import ConnectTimeout

URL = 'https://music.163.com/artist?id='

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
}

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'yun_music'
MONGO_COLLECTION = 'music'
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
db_collection = db[MONGO_COLLECTION]


def get_page(id):
    url = URL + str(id)
    try:
        response = requests.get(url, headers=HEADERS)
        return response.text
    except ConnectTimeout as e:
        print(e.response, e.args)


def parse_html(html):
    doc = pq(html)
    # music = doc('ul.f-hide li').text().replace(' - ', '-').replace(' (', '(').split(' ')
    music_data = json.loads(doc('#song-list-pre-data').text())
    for music in music_data:
        yield {
            'name': music['name'],
            'album_name': music['album']['name'],
            'duration': music['duration'],
            'picUrl': music['album']['picUrl']
        }


def save_music(music):
    try:
        if db_collection.insert_one(music):
            print('存储到mongodb成功')
    except Exception:
        print('存储到monogdb失败')


if __name__ == '__main__':
    html = get_page(3683)
    result = parse_html(html)
    for data in result:
        save_music(data)

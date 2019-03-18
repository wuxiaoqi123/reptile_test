# coding=utf-8
import requests

url = 'https://m.so.com/index.php?q='

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
}


def index(key):
    requesturl = url + key
    response = requests.get(requesturl,headers=headers)
    if(response.status_code == 200):
        print(response.text)


if __name__ == '__main__':
    index('百度')
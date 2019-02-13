# coding=utf-8
import requests
from pyquery import PyQuery as pq

url = 'http://tool.oschina.net/commons'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36',
}

map = {}

response = requests.get(url=url, headers=headers)
if (response.status_code == 200):
    html = response.text
    # print(html)
    doc = pq(html)
    # items = doc('.separateColor').items()
    items = doc('tr').items()
    list_items = []
    for item in items:
        list_items.append(item.text())
    # print(list_items)
    for item in list_items:
        split = item.split()
        map[split[0]] = split[1]
        map[split[2]] = split[3]
    # print(json.dumps(map))
    print()
    content = input('请输入要查询的文件后缀(例.html):')
    get = map.get(content)
    if get == None:
        print('未查询到匹配的content-type')
    else:
        print(get)


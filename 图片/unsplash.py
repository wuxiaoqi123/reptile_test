# coding=utf-8
import time
from contextlib import closing

import requests


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Mobile Safari/537.36',
#     'authority': 'unsplash.com',
# }
#
# response = requests.get(url='https://unsplash.com/napi/photos?page=0&per_page=12', headers=headers)
# if response.status_code == 200:
#     html_json = response.json()
#     for item in html_json:
#         print(item['urls']['full'])

class get_photos(object):

    def __init__(self, start_page=0, end_page=10, per_page=12):
        self.start_page = start_page
        self.end_page = end_page
        self.per_page = per_page
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Mobile Safari/537.36',
            'authority': 'unsplash.com',
        }

    def get_down_url(self):
        for page in range(self.end_page):
            target = self.start_page + page
            print('target:' + str(target))
            self.down_server = 'https://unsplash.com/napi/photos?page=' + str(target) + '&per_page=' + str(
                self.per_page)
            response = requests.get(url=self.down_server, headers=self.headers)
            if response.status_code == 200:
                res_json = response.json()
                for item in res_json:
                    try:
                        yield item['urls']['full']
                    except:
                        pass

    def down_photo(self, url):
        with closing(requests.get(url=url, headers=self.headers, stream=True)) as r:
            with open('%d.jpg' % int(time.time()), 'ab+') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()


if __name__ == '__main__':
    photo = get_photos()
    for down_url in photo.get_down_url():
        photo.down_photo(down_url)

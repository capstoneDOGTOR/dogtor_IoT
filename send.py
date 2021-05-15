import requests

class send():
    def __init__(self, uid):
        self.uid = uid

    def send_json(self, data, where):
        URL = 'http://13.209.18.94:3000/' + where

        res = requests.post(URL, json=data, headers={'Authorization': self.uid})
        # print('POST    :', res.status_code)
        # print(res.text)
        return res


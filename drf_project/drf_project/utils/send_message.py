import requests

from drf_project.utils.contastnt import API_KEY


class Message(object):

    def __init__(self):
        #账号唯一标识
        self.api_key = API_KEY
        #单挑短信接口
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_message(self, phone, code):
        params = {
            'apikey': self.api_key,
            'mobile': phone,
            'text': "【毛信宇test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        req = requests.post(self.single_send_url, data=params)


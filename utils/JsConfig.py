# 手机扫一扫功能调用接口
import hashlib
import time, requests
from django.conf import settings
from utils.my_request import MyRequest


class JsApiConfig(MyRequest):

    @property
    def JsapiTicket(self):
        return settings.WX_JSAPITICKET['token']

    def get_config(self, params):
        noncestr = 'Wm3WZYTPz0wzccnWaa'
        timestamp = int(time.time())
        # 保存ticket过期不验证
        if not self.Token or self.Token != settings.WX_JSAPITICKET['token']:
            settings.WX_JSAPITICKET['token'] = self.Token
            jsapiticket = self.get_QyTicket()
        else:
            jsapiticket = self.JsapiTicket
        api_str = 'jsapi_ticket={JSAPITICKET}&noncestr={NONCESTR}&timestamp={TIMESTAMP}&url={URL}'.format(
            JSAPITICKET=jsapiticket, NONCESTR=noncestr, TIMESTAMP=timestamp, URL=params['url']
        )
        sha = hashlib.sha1(api_str.encode('utf-8'))
        encrypts = sha.hexdigest()
        params.update({'nonceStr': noncestr, 'timestamp': timestamp, 'signature': encrypts, 'appId': 'wwa84b8b2c3e83d6e0'})
        return params


    def get_QyTicket(self):
        _url ='https://qyapi.weixin.qq.com/cgi-bin/get_jsapi_ticket?access_token={ACCESS_TOKEN}'
        if not self.Token:
            self.get_token()
        res = requests.get(_url.format(ACCESS_TOKEN=self.Token)).json()
        settings.WX_JSAPITICKET['ticket'] = res['ticket']
        return res['ticket']


if __name__ == '__main__':
    a = JsApiConfig()
    # a.get_QyTicket()
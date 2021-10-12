# 企业微信验证链接
import requests
from django.conf import settings


class MyRequest:

    @property
    def Token(self):
        # result = {'access_token': 'RoKJvF8toW2l2huxJuJORdZq7OjLS2jDgW6dd3Up7QV07mOpfgFQP1YNaaGMIXzgD1AZN_vxE_ds3_BKpyJeiUZGz9kFH5YmXINLy3uVaZcrQHui3AxXK_Zz3OXDWdQQ2rlq4VoNnjpl4iWUsJZdr1eTQsPgNEJnpRA5lJxEPgWmKLgC8luzHSr_OwxnmRBLjRdOcTf51o4sqSJvWzOA2A'}
        # return result['access_token']
        return settings.WX_TOKEN

    def get_token(self):
        ID = 'wwa84b8b2c3e83d6e0'
        SECRET = 'Kge63NyTYnG-1ZS98uzs6FPQsOxDEF6xqDVVEaQz1mM'
        _url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={ID}&corpsecret={SECRET}'
        result = requests.get(_url.format(ID=ID, SECRET=SECRET)).json()
        # result = {'access_token': 'lqvnickfbdNg0NS5_KCiHiSGCtP4e-2F0rkAYJih6smorg6QVApplxfMtcmQ5QTkFatakTg2r5tbjrcewm1JZ-H37AJ4HddD_4VAPSaBsQB1T3OAbBs6IV9yqZs4IJZGY8e03O2457e37TlRuo5YJ7Cg9hWMlK3FCkt9o9f674Y9Ooj-Sj0Yba61H_pajJ6gYl3kU3DZ0qxht4CH-ZffUw'}
        settings.WX_TOKEN = result['access_token']
        return result['access_token']

    def _get_userid(self, code=None):
        _url = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={ACCESS_TOKEN}&code={CODE}'
        print('获取用户名token:', self.Token,code)
        return requests.get(_url.format(ACCESS_TOKEN=self.Token, CODE=code))

    def _get_userInfo(self, userid):
        _url = 'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token={ACCESS_TOKEN}&userid={USERID}'
        # print('获取用户信息TOKEN:%s\n设置的TOKEN:%s'%(self.Token, settings.WX_TOKEN))
        return requests.get(_url.format(ACCESS_TOKEN=self.Token, USERID=userid))

    def get_user(self, code=None):
        data = dict()
        userId = self._get_userid(code).json()
        print('用户名返回值', userId)
        # userId = {'errcode': 0, 'UserId': 'ZhouWenXing', 'errmsg': 'ok'}
        if userId['errcode'] == 41001 or userId['errcode'] == 42001:
            self.get_token()
            # print(self.Token)
            data['usr'] = self._update_user(self._get_userid(code).json())
            data.update(userId)
            return data
        elif userId['errcode'] == 0:
            # print('拿到用户', userId)
            data['usr'] = self._update_user(userId)
            data.update(userId)
            return data
        else:
            # print('其它', userId)
            data['usr'] = None
            data.update(userId)
            return data

    def get_info(self, userid):
        user_info = self._get_userInfo(userid).json()
        # print('userinfo', user_info)
        if 'userid' in user_info:
            user_info.update({'username':user_info.pop('userid')})
            return user_info
        else:
            return user_info

    def _update_user(self, userid):
        if userid['errcode'] == 0:
            user = userid['UserId'] if ('UserId' in userid) else userid['OpenId']
            return user
        return None


class TestRequest:

    def get_token(self):
        ID = 'wwa84b8b2c3e83d6e0'
        SECRET = 'Kge63NyTYnG-1ZS98uzs6FPQsOxDEF6xqDVVEaQz1mM'
        _url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={ID}&corpsecret={SECRET}'
        result = requests.get(_url.format(ID=ID, SECRET=SECRET)).json()
        return result

    def get_department(self, access_token, Id=None):
        _url = 'https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token={ACCESS_TOKEN}'
        result = requests.get(_url.format(ACCESS_TOKEN=access_token)).json()
        return result
# 推送消息
import requests,json, datetime
from django.db.models import Q

from utils.my_request import MyRequest
from engineering import models as e_models


def push_m(d):
    request = MyRequest()
    if request.Token:
        # print('不空')
        # print(request.Token)
        send_message(request.Token, d)
    else:
        # print('空')
        request.get_token()
        # print(request.Token)
        send_message(request.Token, d)


def send_message(token, d=None):
    t = datetime.datetime.now()
    if 'user_list' in d and d['user_list']:
        # 卡片
        t_data = {
            "touser": d['user_list'],
            "toparty": "",
            "totag": "",
            "msgtype": "textcard",
            "agentid": 1000007,
            "textcard": {
                "title": "您的关注的 < {} >".format(d['project_name']),
                "description": "<div class=\"gray\">{}</div> {}"
                               "{}".format(
                    t.strftime('%Y-%m-%d %H:%M:%S'), d['user'], d['content']
                ),
                "url": "http://test.windit.com.cn/pm/showProject?id=%s" % d['project_id'],
                "btntxt": "点击查看详情",
            },
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        # markdown
        # t_data = {
        #     "touser": d['user_list'],
        #     "toparty": "",
        #     "totag": "",
        #     "msgtype": "markdown",
        #     "agentid": 1000007,
        #     "markdown": {
        #         "content": """您的关注的{project}\n> **最新情况**\n> 更新时间：<font color=\"comment\"> {time}</font> \n> \n>{content} \n>请点击：[查看信息]({url})"""
        #                        .format(project=d['project_name'],content=d['content'],time=t.strftime('%Y-%m-%d %H:%M:%S'),
        #                                 url="http://test.windit.com.cn/pm/showProject?id=%s"%d['project_id'],
        #                                ),
        #     },
        #     "enable_duplicate_check": 0,
        #     "duplicate_check_interval": 1800
        # }
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(token)
        print(requests.post(url=url, data=json.dumps(t_data)).text)


# 通知收藏的人
def test_messages(data, project_obj, user_obj, userID):
    # print('推送：%s'%data['project'])
    project_name = project_obj.filter(id=data['project']).first()
    if 'content' in data and data['content']:
        content = '<div class=\"normal\"></div>'
        for v in data['content'].split('\n'):
            content += '<div class=\"normal\">{}</div>'.format(v)
    else:
        content = '项目信息更新了'
    collect = [v['collect'] for v in project_obj.filter(id=data['project']).values('collect')
               if v['collect']]
    manager = [ v['manager'] for v in project_obj.filter(id=data['project']).values('manager') if v['manager']]
    salesman = [v['salesman'] for v in project_obj.filter(id=data['project']).values('salesman') if v['salesman']]
    diagnosisman = [v['diagnosisman'] for v in project_obj.filter(id=data['project']).values('diagnosisman') if
                    v['diagnosisman']]
    builders = [v['builders'] for v in project_obj.filter(id=data['project']).values('builders') if
                    v['builders']]
    # user_list = '|'.join([v['username'] for v in user_obj.filter(id__in=collect).values()])
    users = salesman+diagnosisman+builders+collect
    users += [v['id'] for v in user_obj.filter(name__in=manager).values('id') if 'id' in v]
    print(users)
    print(userID.id, userID.name)
    user_list = '|'.join([v['username'] for v in user_obj.filter(id__in=users).exclude(username=userID).values('username')])
    res = {
        'project_id': data['project'],
        'project_name':project_name,
        'user_list': user_list,
        'content': content,
        'user':userID.name
    }
    push_m(res)
    return
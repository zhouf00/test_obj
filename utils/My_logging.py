# 日报记录
from utils.response import APIResponse
from personnel import models as p_models
from engineering import models as e_models
from utils.Push_message import  test_messages


def logit(fun):
    def inner(request, *args, **kwargs):
        if fun.__name__ == 'get' or fun.__name__ == 'list':
            try:
                a = fun(request, *args, **kwargs)
                return a[1]
            except Exception as e:
                print(e.args[0])
                return APIResponse(
                    data_msg='get error',
                    results={'error': e.args[0]}
                )
        elif fun.__name__ == 'create' or fun.__name__ == 'update':
            try:
                res = fun(request, *args, **kwargs)
                if 'project' not in res[1]:
                    res[1]['project'] = res[1]['id']
                project_obj = e_models.Project.objects.all()
                user_obj = p_models.User.objects.all()
                test_messages(res[1], project_obj, user_obj, res[0]['userId'])
                return APIResponse(
                    data_msg='update ok',
                    results=res[1]
                )
            except Exception as e:
                print('error:',e.args[0])
                return APIResponse(
                    data_msg='update error',
                    results={'error': e.args[0]}
                )
    return inner
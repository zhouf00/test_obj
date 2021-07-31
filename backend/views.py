from rest_framework.views import APIView
from utils.JsConfig import JsApiConfig
from utils.response import APIResponse

from engineering import models as e_models

# Create your views here.

class JsApiAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request, *args, **kwargs):
        params = request.data
        jsapi = JsApiConfig()
        config = jsapi.get_config(params)
        return APIResponse(
            data_msg='jsapi ok',
            results=config
        )


class PushMessageAPIView(APIView):

    def post(self, request,  *args, **kwargs):
        data = request.data
        worklog_list = []
        if data['d']['id']:
            worklog_list.append(data['d']['id'])
        if data['d']['ln_worklog']:
            worklog_list.append(data['d']['ln_worklog'])
        print('推送')
        print(worklog_list)
        print(e_models.ProjectTrace.objects.filter(worklog__in=worklog_list))
        print(data['d'])
        print('===========')
        # print(e_models.Project.objects.filter())
        return APIResponse(

        )
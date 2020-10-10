from rest_framework.views import APIView
from utils.JsConfig import JsApiConfig
from utils.response import APIResponse

# Create your views here.

class JsApiAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request, *args, **kwargs):
        params = request.data
        print(params)
        jsapi = JsApiConfig()
        config = jsapi.get_config(params)
        print(config)
        return APIResponse(
            data_msg='jsapi ok',
            results=config
        )
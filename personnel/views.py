from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, mixins
from rest_framework.response import Response

from personnel import models, serializers
from utils.my_modelview import MyModelViewSet

class UserViewSet(ModelViewSet):

    queryset = models.User.objects.all()
    serializer_class = serializers.UserModelSerializer


class DeptViewSet(ModelViewSet, MyModelViewSet):
    # 未完成群改功能
    queryset = models.Structure.objects.all()
    serializer_class = serializers.DeptModelSerializer

    def my_post(self, request, *args, **kwargs):
        serializer = serializers.DeptModelSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    def my_patch(self, request, *args, **kwargs):
        instance, request_data = self.get_myinstance(request, *args, **kwargs)
        serializer = serializers.DeptModelSerializer(instance=instance, data=request.data, partial=False, many=True)
        serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)

        return Response({
            'status': 1,
            'msg': '成功'
        })



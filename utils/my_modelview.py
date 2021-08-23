# 网页模型
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from engineering.serializers import ProjectUpdateTime
from engineering.models import Project

from utils.response import APIResponse
from utils.My_logging import logit


# 项目更新加完成状态更改
def UpdateTime(data):
    print('更新',data)
    id = data['project']
    updateTmp = {}
    if 'finish' in data and data['finish']:
        project_obj = Project.objects.filter(pk=id)
        finish_list = ['未完成' for var in project_obj.values('stock__finish') if var['stock__finish']!= 2]
        if '未完成' in finish_list:
            updateTmp['stock_finish'] = '未完成'
        else:
            updateTmp['stock_finish'] = '完成'
    else:
        return
    project_ser = ProjectUpdateTime(instance=project_obj.first(), data=updateTmp)
    project_ser.is_valid(raise_exception=True)
    project_ser.save()


# 使用后更新项目的最新日期
class MyProjectModelViewSet(ModelViewSet):

    @logit
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if 'project' in request.data and request.data['project']:
            UpdateTime(serializer.data)
        return ({
            'userId': self.request.user.id,
            'name': self.request.user.name
                }
            ,serializer.data)

    @logit
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if 'project' in request.data and request.data['project']:
            UpdateTime(serializer.data)
        return (self.request.user
        , serializer.data)

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from engineering.serializers import ProjectUpdateTime
from engineering.models import Project

from utils.response import APIResponse


# 项目更新加完成状态更改
def UpdateTime(data):
    id = data['project']
    updateTmp = {'priority': 1}
    project_obj = Project.objects.filter(pk=id)
    if 'finish' in data and data['finish']:
        finish_list = ['未完成' for var in project_obj.values('stock__finish') if var['stock__finish']!= 2]
        if '未完成' in finish_list:
            updateTmp['stock_finish'] = '未完成'
        else:
            updateTmp['stock_finish'] = '完成'
    print(project_obj, updateTmp)
    project_ser = ProjectUpdateTime(instance=project_obj.first(), data=updateTmp)
    project_ser.is_valid(raise_exception=True)
    project_ser.save()


# 使用后更新项目的最新日期
class ProjectUpdateViewSet(ModelViewSet):

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        if 'project' in request.data and request.data['project']:
            UpdateTime(request.data)
        return APIResponse(
            data_msg='create ok',
            results=request.data
        )

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        if 'project' in request.data and request.data['project']:
            UpdateTime(request.data)
        return APIResponse(
            data_msg='update ok',
            results=request.data
        )

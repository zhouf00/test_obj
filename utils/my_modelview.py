from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from engineering.serializers import ProjectUpdateTime
from engineering.models import Project

from utils.response import APIResponse

def UpdateTime(id):

    project_obj = Project.objects.filter(pk=id)
    finish_list = ['未完成' for var in project_obj.values('stock__finish') if var['stock__finish']!= 2]
    if not '未完成' in finish_list:
        stock_finish = '完成'
    project_ser = ProjectUpdateTime(instance=project_obj.first(), data={'priority': 1,'stock_finish': stock_finish})
    project_ser.is_valid(raise_exception=True)
    project_ser.save()


# 使用后更新项目的最新日期
class ProjectUpdateViewSet(ModelViewSet):

    def create(self, request, *args, **kwargs):
        if 'project' in request.data and request.data['project']:
            UpdateTime(request.data['project'])
        super().create(request, *args, **kwargs)
        return APIResponse(
            data_msg='create ok',
            results=request.data
        )

    def update(self, request, *args, **kwargs):
        if 'project' in request.data and request.data['project']:
            UpdateTime(request.data['project'])
        super().update(request, *args, **kwargs)
        return APIResponse(
            data_msg='update ok',
            results=request.data
        )

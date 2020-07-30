from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from engineering import models, serializers


class ProjectViewSet(ModelViewSet):
    """项目列表数据"""
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectModelSerializer


class DetailViewSet(ModelViewSet):
    """详情页面数据"""
    queryset = models.Project.objects.filter(is_delete=False)
    serializer_class = serializers.DetailModelSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields =['id', 'name']


class ServerViewSet(ModelViewSet):
    """服务器数据"""
    queryset = models.Server.objects.filter(is_delete=False)
    serializer_class = serializers.ServerModelSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields =['project']


class FacilityViewSet(ModelViewSet):
    """风机数据"""
    queryset = models.Facility.objects.filter(is_delete=False)
    serializer_class = serializers.FacilityModelSerializer


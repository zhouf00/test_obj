from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from engineering import models, serializers, filters
from utils.response import APIResponse
from utils.authentications import JWTAuthentication
from utils.pagenations import MyPageNumberPagination


class ProjectViewSet(ModelViewSet):
    """项目列表数据"""
    queryset = models.Project.objects.filter(is_delete=False).order_by()
    serializer_class = serializers.ProjectModelSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    pagination_class = MyPageNumberPagination
    filter_class = filters.ProjectFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields =['id', 'name', 'area', 'sn']


class ProjectCreateViewSet(ModelViewSet):

    queryset = models.Project.objects.all()
    serializer_class = serializers.CreateProjectModelSerializer

    def create(self, request, *args, **kwargs):
        super().create(request,*args, **kwargs)


class CollectorViewSet(ModelViewSet):

    queryset = models.Collector.objects.all()
    serializer_class = serializers.CollectorModelSerializer


class AisleViewSet(ModelViewSet):

    queryset = models.Aisle.objects.all()
    serializer_class = serializers.AisleModelSerializer


class ProjectManufacturerViewSet(ModelViewSet):

    queryset = models.Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerModelSerializer


class MonitorTypeViewSet(ModelViewSet):

    queryset = models.MonitorType.objects.all()
    serializer_class = serializers.MonitorTypeModelSerializer


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


class CpuViewSet(ModelViewSet):

    queryset = models.CPU.objects.filter(is_delete=False)
    serializer_class = serializers.CpuModelSerializer


class RamViewSet(ModelViewSet):

    queryset = models.RAM.objects.filter(is_delete=False)
    serializer_class = serializers.RamModelSerializer


class DiskViewSet(ModelViewSet):

    queryset = models.Disk.objects.filter(is_delete=False)
    serializer_class = serializers.DiskModelSerializer


class NicViewSet(ModelViewSet):

    queryset = models.NIC.objects.filter(is_delete=False)
    serializer_class = serializers.NicModelSerializer


class FacilityViewSet(ModelViewSet):
    """风机数据"""
    queryset = models.Facility.objects.filter(is_delete=False)
    serializer_class = serializers.FacilityModelSerializer


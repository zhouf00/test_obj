from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from engineering import models, serializers, filters
from utils.response import APIResponse
from utils.authentications import JWTAuthentication
from utils.pagenations import MyPageNumberPagination
from utils.my_modelview import ProjectUpdateViewSet


class ProjectViewSet(ModelViewSet):
    """项目列表数据"""
    queryset = models.Project.objects.filter(is_delete=False).order_by('-update_time')
    serializer_class = serializers.ProjectModelSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    pagination_class = MyPageNumberPagination
    filter_class = filters.ProjectFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]


class ProjectCreateViewSet(ModelViewSet):

    queryset = models.Project.objects.all().order_by('id')
    serializer_class = serializers.CreateProjectModelSerializer


class IdcRoomViewSet(ProjectUpdateViewSet):

    queryset = models.IdcRoom.objects.all().order_by('id')
    serializer_class = serializers.IdcRoomModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.IdcRoomFilterSet


class ProjectManufacturerViewSet(ModelViewSet):

    queryset = models.Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerModelSerializer


class ContractViewSet(ModelViewSet):

    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractModelSerializer

    filter_class = filters.ContractFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]


class OutsourcerViewSet(ModelViewSet):

    queryset = models.Outsourcer.objects.all()
    serializer_class = serializers.OutsourcerModelSerializer


class StockViewSet(ProjectUpdateViewSet):

    queryset = models.Stock.objects.all().order_by('id')
    serializer_class = serializers.StockModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.StockFilterSet


class InvoiceViewSet(ProjectUpdateViewSet):

    queryset = models.Invoice.objects.all().order_by('-create_time')
    serializer_class = serializers.InvoiceModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.InvoiceFilterSet


class InvoiceImageViewSet(ProjectUpdateViewSet):

    queryset = models.InvoiceImage.objects.all()
    serializer_class = serializers.InvoiceImageModelSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['invoice__id']


class ProjectTraceViewSet(ProjectUpdateViewSet):

    queryset = models.ProjectTrace.objects.all().order_by('-create_time')
    serializer_class = serializers.ProjectTraceModelSerializer

    filter_class = filters.ProjectTraceFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]



######
# 标签组
#####
class MonitorTypeViewSet(ModelViewSet):

    queryset = models.MonitorType.objects.all()
    serializer_class = serializers.MonitorTypeModelSerializer


class ProjectTypeViewSet(ModelViewSet):

    queryset = models.ProjectType.objects.all()
    serializer_class = serializers.ProjectTypeModelSerializer


class ProjectStatusViewSet(ModelViewSet):

    queryset = models.ProjectStatus.objects.all()
    serializer_class = serializers.ProjectStatusModelSerializer


class ProjectAreaViewSet(ModelViewSet):

    queryset = models.ProjectArea.objects.all()
    serializer_class = serializers.ProjectAreaModelSerializer


class ProjectWorkingEnvViewSet(ModelViewSet):

    queryset = models.ProjectWorkingEnv.objects.all()
    serializer_class = serializers.ProjectWorkingEnvModelSerializer


class StockFinishViewSet(ModelViewSet):

    queryset = models.StockFinish.objects.all()
    serializer_class = serializers.StockModelSerializer


class MonitorNumberViewSet(ModelViewSet):

    queryset = models.MonitorNumber.objects.all()
    serializer_class = serializers.MonitorNumberModelSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['project__id']
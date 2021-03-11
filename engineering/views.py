import time
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum

from engineering import models, serializers, filters
from personnel import models as personnel_models

from utils.response import APIResponse
from utils.pagenations import MyPageNumberPagination
from utils.my_modelview import ProjectUpdateViewSet


class ProjectViewSet(ModelViewSet):
    """项目列表数据"""
    queryset = models.Project.objects.filter(is_delete=False).order_by('-update_time')
    serializer_class = serializers.ProjectModelSerializer

    pagination_class = MyPageNumberPagination
    filter_class = filters.ProjectFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]

    def get_queryset(self):
        super().get_queryset()
        # 拿到管理员身份
        role = self.request.user.roleList
        if '超级管理员' in role:
            # print('你是管理员')
            pass
        elif '普通用户'in role and len(role)>1:
            pass
        else:
            pass
            # 拿到部门领导身份
            if self.request.user.deptList:
                # print('你是部门领导')
                # self.isleader = True
                self.queryset = self.queryset.filter(manager__in=self.request.user.deptmembers[1]).distinct()
            else:
                # print('你不是部门领导')
                # self.isleader = False
                self.queryset = self.queryset.filter(manager=self.request.user.name).distinct()
        return self.queryset


class ProjectClassifyViewSet(GenericViewSet):

    queryset = models.Project.objects.filter(is_delete=False).order_by('-update_time')
    serializer_class = serializers.ProjectModelSerializer

    pagination_class = MyPageNumberPagination
    filter_class = filters.ProjectFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]

    def get_queryset(self):
        # 拿到管理员身份
        role = self.request.user.roleList
        if '超级管理员' in role:
            # print('你是管理员')
            pass
        elif '普通用户'in role and len(role)>1:
            pass
        else:
            pass
            # 拿到部门领导身份
            if self.request.user.deptList:
                # print('你是部门领导')
                # self.isleader = True
                self.queryset = self.queryset.filter(manager__in=self.request.user.deptmembers[1]).distinct()
            else:
                # print('你不是部门领导')
                # self.isleader = False
                self.queryset = self.queryset.filter(manager=self.request.user.name).distinct()
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset)
        tag_list = list(models.ProjectStatus.objects.values('title', 'id').order_by('sort'))

        for var in tag_list:
            var.update({
                'count':queryset.filter(status__title=var['title']).count(),
                'facility_count':queryset.filter(status__title=var['title']).aggregate(count=Sum('facility_count'))['count']
            })
        tag_list.append({
            'title': '项目总数',
            'id': 0,
            'count': queryset.count(),
            'facility_count': queryset.aggregate(count=Sum('facility_count'))['count']
        })
        return APIResponse(results=tag_list)


class ProjectOverview(APIView):

    queryset = models.Project.objects.filter(is_delete=False).order_by('-update_time')
    query_user = personnel_models.User.objects.exclude(id=1)

    def get(self, request, *args, **kwargs):
        project_dict = {}

        queryset = self.queryset.filter(Q(builders__isnull=False) |Q(priority__isnull=False)).values(
            'id', 'name', 'priority__title', 'province', 'status__title', 'builders__name','update_time')
        query_user = self.query_user.filter(project__isnull=True).filter(department__in=[6]).filter(is_active=1)
        users = []
        # print(users)
        user_list = users
        for var in queryset:
            # print(var)
            if 'id' in project_dict and var['id'] in project_dict :
                project_dict[var['id']]['builders'] += '%s'%var['builders__name']
            else:
                project_dict[var['id']] = {
                    'id': var['id'],
                    'name':var['name'],
                    'province':var['province'],
                    'priority': var['priority__title'],
                    'status': var['status__title'],
                    'builders': var['builders__name'],
                    'update_time': var['update_time'].strftime('%Y-%m-%d'),
                }
            if var['builders__name']:
                user_list.append({
                    'id': var['id'],
                    'name': var['name'],
                    'province': var['province'],
                    'priority': var['priority__title'],
                    'status': var['status__title'],
                    'builders': var['builders__name'],
                    'update_time': var['update_time'].strftime('%Y-%m-%d '),
                })
        user_list+=[{'builders': var['name'], 'status': '待命'} for var in query_user.values('name')]
        res = {
            'project': project_dict.values(),
            'user': user_list
        }
        return APIResponse(results=res)


class ProjectCreateViewSet(ModelViewSet):

    queryset = models.Project.objects.all().order_by('id')
    serializer_class = serializers.CreateProjectModelSerializer


class ProjectStatusTimeViewSet(ModelViewSet):
    queryset = models.ProjectStatusTime.objects.all()
    serializer_class = serializers.ProjectStatusTimeSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.ProjectStatusTimeFilterSet

    def my_post(self, request, *args, **kwargs):
        request_data = request.data
        # 没有时创建
        if not self.queryset.filter(Q(project=request_data['project']) & Q(status_id=request_data['status'])):
            serializer = self.get_serializer(data=request_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            partial = kwargs.pop('partial', False)
            instance = self.queryset.filter(Q(project=request_data['project']) & Q(status_id=request_data['status'])).first()
            serializer = self.get_serializer(instance, data=request_data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        models.Project.objects.update_or_create(defaults={'status_id':request_data['status']},pk=request_data['project'])
        return APIResponse(results=request_data)


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

    queryset = models.Outsourcer.objects.all().order_by('id')
    serializer_class = serializers.OutsourcerModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.OutsourcerFilterSet


class OutsourcerListViewSet(ModelViewSet):

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


class InvoiceUpdateViewSet(ModelViewSet):

    queryset = models.Invoice
    serializer_class = serializers.InvoiceUpdateModelSerializer


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
class ProjectPriorityViewSet(ModelViewSet):

    queryset = models.ProjectPriority.objects.all()
    serializer_class = serializers.ProjectPrioritySerializer


class MonitorTypeViewSet(ModelViewSet):

    queryset = models.MonitorType.objects.all()
    serializer_class = serializers.MonitorTypeModelSerializer


class ProjectTypeViewSet(ModelViewSet):

    queryset = models.ProjectType.objects.all()
    serializer_class = serializers.ProjectTypeModelSerializer


class ProjectStatusViewSet(ModelViewSet):

    queryset = models.ProjectStatus.objects.all().order_by('sort')
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

    filter_class = filters.MonitorNumberFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]


class TraceStatusViewSet(ModelViewSet):

    queryset = models.TraceStatus.objects.all()
    serializer_class = serializers.TraceStatusSerializer


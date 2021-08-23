from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum

from engineering import models, serializers, filters
from personnel import models as personnel_models

from utils.response import APIResponse
from utils.pagenations import MyPageNumberPagination
from utils.my_modelview import MyProjectModelViewSet


# 项目信息
class ProjectViewSet(MyProjectModelViewSet):
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
            # 拿到部门领导身份
            if self.request.user.deptList:
                # print('你是部门领导')
                # self.isleader = True
                self.queryset = self.queryset.filter(
                    Q(manager__in=self.request.user.deptmembers[1]) |
                    Q(builders__in=self.request.user.deptmembers[2]) |
                    Q(salesman__in=self.request.user.deptmembers[2]) |
                    Q(diagnosisman__in=self.request.user.deptmembers[2])
                ).distinct()
            else:
                # print('你不是部门领导')
                # self.isleader = False
                self.queryset = self.queryset.filter(
                    Q(manager=self.request.user.name) |
                    Q(builders=self.request.user.id) |
                    Q(salesman=self.request.user.id) |
                    Q(diagnosisman=self.request.user.id)
                ).distinct()
        return self.queryset


class ProjectDeleteViewSet(ModelViewSet):
    queryset = models.Project.objects.filter(is_delete=False).order_by('-amount')
    serializer_class = serializers.ProjectDeleteModelSerializer


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
                self.isleader = True
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
            # print(var['id'] in project_dict.keys())
            if var['id'] in project_dict.keys() :
                project_dict[var['id']]['builders'] += ',%s'%var['builders__name']
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


class ProjectListViewSet(ModelViewSet):
    queryset = models.Project.objects.all().order_by('id')
    serializer_class = serializers.ProjectListModelSerializer


# 监测设备信息
class FacilityViewSet(ModelViewSet):

    queryset = models.Facility.objects.all().order_by('id')
    serializer_class = serializers.FacilityModelSerializer

    filter_class = filters.FacilityFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]


class ProjectStatusTimeViewSet(ModelViewSet):
    queryset = models.ProjectStatusTime.objects.all().order_by('time')
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


class IdcRoomViewSet(MyProjectModelViewSet):

    queryset = models.IdcRoom.objects.all().order_by('id')
    serializer_class = serializers.IdcRoomModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.IdcRoomFilterSet


class ProjectManufacturerViewSet(ModelViewSet):

    queryset = models.Manufacturer.objects.all()
    serializer_class = serializers.ManufacturerModelSerializer


class ContractViewSet(MyProjectModelViewSet):

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


class StockViewSet(MyProjectModelViewSet):

    queryset = models.Stock.objects.all().order_by('id')
    serializer_class = serializers.StockModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.StockFilterSet


class InvoiceViewSet(MyProjectModelViewSet):

    queryset = models.Invoice.objects.all().order_by('-create_time')
    serializer_class = serializers.InvoiceModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.InvoiceFilterSet


class InvoiceUpdateViewSet(ModelViewSet):

    queryset = models.Invoice
    serializer_class = serializers.InvoiceUpdateModelSerializer


class InvoiceImageViewSet(MyProjectModelViewSet):

    queryset = models.InvoiceImage.objects.all()
    serializer_class = serializers.InvoiceImageModelSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.InvoiceImageFilterSet


class ProjectTraceViewSet(MyProjectModelViewSet):

    queryset = models.ProjectTrace.objects.all().order_by('-create_time')
    serializer_class = serializers.ProjectTraceModelSerializer

    filter_class = filters.ProjectTraceFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        # 关联信息
        user_list = personnel_models.User.objects.exclude(id=1)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.add_user(serializer.data, user_list)
        return APIResponse(
            data_msg='post ok',
            results=serializer.data)

    def add_user(self,data, user_list):
        for var in data:
            user = user_list.filter(id=var['user']).values('id','name', 'avatar').first()
            var['userInfo'] = user if user else {}
            var['subscriberList'] = user_list.filter(id__in=var['subscriber']).values('id','name', 'avatar')


# 收藏
class ProjectColletViewSet(APIView):

    def post(self, request, *args, **kwargs):
        d = request.data
        # print(d)
        project_obj = models.Project.objects.filter(id=d[0])
        collect = [v['collect'] for v in project_obj.values('collect') if v['collect']]
        # collect = [2,3]
        if d[1]:
            if d[2] not in collect:
                collect.append(d[2])
            else:
                pass
        else:
            collect.remove(d[2])
        # print(collect)
        project_ser = serializers.ProjectCollect(instance=project_obj.first(), data={'collect':collect})
        project_ser.is_valid(raise_exception=True)
        project_ser.save()
        # print(project_ser.data)
        return APIResponse(
            data_msg='collect ok',
            results=project_ser.data
        )

######
# 标签组
#####
class ProjectPriorityViewSet(ModelViewSet):

    queryset = models.ProjectPriority.objects.all().order_by('sort')
    serializer_class = serializers.ProjectPrioritySerializer


class ProjectPriority2ViewSet(ModelViewSet):

    queryset = models.ProjectPrority2.objects.all().order_by('sort')
    serializer_class = serializers.ProjectPriority2Serializer


class MonitorTypeViewSet(ModelViewSet):

    queryset = models.MonitorType.objects.all().order_by('sort')
    serializer_class = serializers.MonitorTypeModelSerializer


class ProjectTypeViewSet(ModelViewSet):

    queryset = models.ProjectType.objects.all().order_by('sort')
    serializer_class = serializers.ProjectTypeModelSerializer


class ProjectStatusViewSet(ModelViewSet):

    queryset = models.ProjectStatus.objects.all().order_by('sort')
    serializer_class = serializers.ProjectStatusModelSerializer


class ProjectAreaViewSet(ModelViewSet):

    queryset = models.ProjectArea.objects.all().order_by('sort')
    serializer_class = serializers.ProjectAreaModelSerializer


class ProjectWorkingEnvViewSet(ModelViewSet):

    queryset = models.ProjectWorkingEnv.objects.all().order_by('sort')
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

    queryset = models.TraceStatus.objects.all().order_by('sort')
    serializer_class = serializers.TraceStatusSerializer


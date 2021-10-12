# django-filter过滤器
import datetime
from django_filters.rest_framework.filterset import FilterSet
# 自定义过滤字段
from django_filters import filters
from django.db.models import Q
from . import models
from personnel import models as p_models


# 自定义过滤器，接口：?limit=显示的条数
class LimitFilter:
    def filter_queryset(self, request, queryset, view):
        limit = request.query_params.get('limit')
        if limit:
            limit = int(limit)
            return queryset[:limit]
        return queryset


class TaskFilter(FilterSet):

    title = filters.CharFilter(field_name='title',lookup_expr='icontains')
    users = filters.CharFilter(method='filter_users')
    tasks = filters.CharFilter(method='filter_tasks')

    user = filters.CharFilter(method='filter_user')
    department_list = filters.CharFilter(method='filter_department_list')
    project = filters.CharFilter(field_name='project')
    status_list = filters.CharFilter(method='filter_status')

    def filter_users(self, queryset, name, value):
        return queryset.filter(Q(executor=value) | Q(subscriber=value)).distinct()

    def filter_tasks(self, queryset, name, value):
        value_list = [v for v in value.split(',') if v]
        res = queryset.filter(id__in=value_list) | \
              queryset.filter(Q(executor=self.request.user.id)|Q(subscriber=self.request.user.id))
        return res.distinct()

    def filter_user(self, queryset, name, value):
        obj = p_models.User.objects.filter(name__contains=value).values('id')
        userList = [v['id'] for v in obj]
        return queryset.filter(Q(executor__in=userList) | Q(subscriber__in=userList))

    def filter_department_list(self, queryset, name, value):
        value_list = value.split(',')
        obj = p_models.Structure.objects.filter(deptid__in=value_list).values('users__id')
        userList = [v['users__id'] for v in obj]
        return queryset.filter(Q(executor__in=userList) | Q(subscriber__in=userList))

    def filter_status(self, queryset, name, value):
        value_list = value.split(',')
        res = queryset.filter(status__in=value_list)
        return res

    class Meta:
        model = models.Task
        fields =[]


class TaskfileFilter(FilterSet):
    class Meta:
        model = models.TaskFile
        fields =['task']


class JournalFilter(FilterSet):

    user = filters.CharFilter(method='filter_user')
    department = filters.CharFilter(method='filter_department')
    department_list = filters.CharFilter(method='filter_department')
    work_status_list = filters.CharFilter(method='filter_work_status')
    start_time = filters.DateTimeFilter(field_name='create_time', lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name='create_time', lookup_expr='lte')

    month = filters.CharFilter(method='filter_month')

    def filter_user(self, queryset, name, value):
        obj = p_models.User.objects.filter(name__contains=value).values('id')
        userList = [v['id'] for v in obj]
        return queryset.filter(user__in=userList)

    def filter_department(self, queryset, name, value):
        value_list = value.split(',')
        obj = p_models.Structure.objects.filter(deptid__in=value_list).values('users__id')
        userList = [v['users__id'] for v in obj]
        return queryset.filter(user__in=userList)

    def filter_work_status(self, queryset, name, value):
        value_list = value.split(',')
        return queryset.filter(work_status__in=value_list)

    def filter_month(self, queryset, name, value):
        year, month, day = value.split('-')
        t = datetime.datetime(int(year), int(month), int(day))
        year = t.strftime('%Y')
        month = t.strftime('%m')
        if int(month) == 12:
            end_year = '%d'%(int(year)+1)
            end_month = '1'
        else:
            end_year = year
            end_month = '%d'%(int(month)+1)
        return queryset.filter(create_time__gte="%s-%s-%s"%(year, month, day)).filter(create_time__lte="%s-%s-%s"%(end_year, end_month, day))

    class Meta:
        model = models.WorkLogs
        fields =[]

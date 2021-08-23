# django-filter过滤器
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

    users = filters.CharFilter(method='filter_users')
    tasks = filters.CharFilter(method='filter_tasks')

    user = filters.CharFilter(method='filter_user')
    department = filters.CharFilter(method='filter_department')
    project = filters.CharFilter(field_name='project')

    def filter_users(self, queryset, name, value):
        return queryset.filter(Q(executor=value) | Q(subscriber=value))

    def filter_tasks(self, queryset, name, value):
        value_list = [v for v in value.split(',') if v]
        res = queryset.filter(id__in=value_list) | \
              queryset.filter(Q(executor=self.request.user.id)|Q(subscriber=self.request.user.id))
        return res.distinct()

    def filter_user(self, queryset, name, value):
        obj = p_models.User.objects.filter(name__contains=value).values('id')
        userList = [v['id'] for v in obj]
        return queryset.filter(Q(executor__in=userList) | Q(subscriber__in=userList))

    def filter_department(self, queryset, name, value):
        obj = p_models.Structure.objects.filter(deptid=value).values('users__id')
        userList = [v['users__id'] for v in obj]
        return queryset.filter(Q(executor__in=userList) | Q(subscriber__in=userList))

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

    def filter_user(self, queryset, name, value):
        obj = p_models.User.objects.filter(name__contains=value).values('id')
        userList = [v['id'] for v in obj]
        return queryset.filter(user__in=userList)

    def filter_department(self, queryset, name, value):
        obj = p_models.Structure.objects.filter(deptid=value).values('users__id')
        userList = [v['users__id'] for v in obj]
        return queryset.filter(user__in=userList)

    class Meta:
        model = models.WorkLogs
        fields =[]
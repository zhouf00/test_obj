# django-filter过滤器
from django_filters.rest_framework.filterset import FilterSet
# 自定义过滤字段
from django_filters import filters
from django.db.models import Q
from . import models


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

    def filter_users(self, queryset, name, value):
        return queryset.filter(Q(executor=value)|Q(subscriber=value))

    def filter_tasks(self, queryset, name, value):
        value_list = [v for v in value.split(',') if v]
        res = queryset.filter(id__in=value_list) | \
              queryset.filter(Q(executor=self.request.user.id)|Q(subscriber=self.request.user.id))
        return res.distinct()

    class Meta:
        model = models.Task
        fields =[]


class JournalFilter(FilterSet):

    class Meta:
        model = models.WorkLogs
        fields =[]
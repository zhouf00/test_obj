from . import models
# 自定义过滤器，接口：?limit=显示的条数
class LimitFilter:
    def filter_queryset(self, request, queryset, view):
        limit = request.query_params.get('limit')
        if limit:
            limit = int(limit)
            return queryset[:limit]
        return queryset


# django-filter过滤器
import django_filters
from django_filters.rest_framework.filterset import FilterSet
# 自定义过滤字段
from django_filters import filters
class AuthFilterSet(FilterSet):

    name = django_filters.CharFilter(field_name="user__name")

    class Meta:
        model = models.Auth
        fields = ['menu', "user", "name"]

class MenuFilterSet(FilterSet):

    parent = filters.CharFilter(field_name="parent", method='parent_filter')

    def parent_filter(self, queryset, name, value):
        if not int(value):
            value = None
        return queryset.filter(parent=value)

    class Meta:
        model = models.Menu
        fields = ['id','parent']
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
from django_filters.rest_framework.filterset import FilterSet
# 自定义过滤字段
from django_filters import filters

class ProductionFilterSet(FilterSet):

    project = filters.CharFilter(field_name='project__id',)
    sn = filters.CharFilter(field_name='sn')
    # project = filters.CharFilter(method='filter_project')
    #
    # def filter_project(self, queryset, name, value):
    #     print(value)
    #     return queryset.filter()

    class Meta:
        model = models.Production
        fields = []

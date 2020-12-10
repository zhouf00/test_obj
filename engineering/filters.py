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


# 项目筛选
class ProjectFilterSet(FilterSet):

    name = filters.CharFilter(field_name='name',lookup_expr='icontains')
    sn = filters.CharFilter(field_name='sn', lookup_expr='icontains')
    area = filters.CharFilter(field_name='area__id')
    status = filters.CharFilter(field_name='status__id')
    manufacturers = filters.CharFilter(field_name='manufacturers__id')
    stock_finish = filters.CharFilter(field_name='stock_finish')

    class Meta:
        model = models.Project
        fields = ['id', 'name', 'area', 'sn', 'status', 'manufacturers', 'stock_finish']


class OutsourcerFilterSet(FilterSet):

    title = filters.CharFilter(field_name='title',lookup_expr='icontains')

    class Meta:
        model = models.Outsourcer
        fields = ['title']

class IdcRoomFilterSet(FilterSet):

    project = filters.CharFilter(field_name='project__id')

    class Meta:
        model = models.IdcRoom
        fields = ['project']


class StockFilterSet(FilterSet):

    project = filters.CharFilter(field_name='project__id')

    class Meta:
        model = models.Stock
        fields = ['project']


class InvoiceFilterSet(FilterSet):

    project = filters.CharFilter(field_name='project__id')

    class Meta:
        model = models.Invoice
        fields = ['project']


# 项目跟进筛选
class ProjectTraceFilterSet(FilterSet):

    project = filters.CharFilter(field_name='project__id')

    class Meta:
        model = models.ProjectTrace
        fields = ['project']


class ContractFilterSet(FilterSet):

    project = filters.CharFilter(field_name='project__id')

    class Meta:
        model = models.Contract
        fields = ['project']

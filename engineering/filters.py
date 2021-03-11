from . import models
import datetime, time
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
    # manufacturers = filters.CharFilter(field_name='manufacturers__id')
    stock_finish = filters.CharFilter(field_name='stock_finish')
    status_list = filters.CharFilter(method='filter_status_list')
    area_list = filters.CharFilter(method='filter_area_list')
    monitortype_list = filters.CharFilter(field_name='monitor_type')
    user = filters.CharFilter(field_name='manager',lookup_expr='icontains')
    builder = filters.CharFilter(field_name='builders__name', lookup_expr='icontains')
    salesman = filters.CharFilter(field_name='salesman__name', lookup_expr='icontains')
    diagnosisman = filters.CharFilter(field_name='diagnosisman__name', lookup_expr='icontains')
    begin_time = filters.CharFilter(method='filter_begin_time')

    def filter_begin_time(self, queryset, name, value):
        begin_time = time.strftime("%Y", time.localtime(int(value)/1000))
        return queryset.filter(begin_time__year=begin_time)

    def filter_area_list(self, queryset, name, value):
        value_list = value.split(',')
        return queryset.filter(area__id__in=value_list)

    def filter_status_list(self, queryset, name, value):
        value_list = value.split(',')
        return queryset.filter(status__id__in=value_list)

    class Meta:
        model = models.Project
        fields = ['id', 'name', 'area', 'sn', 'status', 'manufacturers', 'stock_finish', 'priority']


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


class MonitorNumberFilterSet(FilterSet):

    project = filters.CharFilter(field_name='project__id')

    class Meta:
        model = models.MonitorNumber
        fields = ['project']


class ProjectStatusTimeFilterSet(FilterSet):

    project = filters.CharFilter(field_name='project__id')

    class Meta:
        model = models.ProjectStatusTime
        fields = ['project']
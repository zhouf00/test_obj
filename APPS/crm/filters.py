# django-filter过滤器
from django_filters.rest_framework.filterset import FilterSet
# 自定义过滤字段
from django_filters import filters
from . import models


# 自定义过滤器，接口：?limit=显示的条数
class LimitFilter:
    def filter_queryset(self, request, queryset, view):
        limit = request.query_params.get('limit')
        if limit:
            limit = int(limit)
            return queryset[:limit]
        return queryset

class MarketFilter(FilterSet):

    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    user = filters.CharFilter(field_name='user__name', lookup_expr='icontains')
    company = filters.CharFilter(field_name='company', lookup_expr='icontains')
    start_time = filters.DateTimeFilter(field_name='traceTime', lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name='traceTime', lookup_expr='lte')

    class Meta:
        model = models.Market
        fields =['hit_rate', 'address']


class LinkmanFilter(FilterSet):

    market = filters.CharFilter(field_name='market__id')

    class Meta:
        model = models.Linkman
        fields = ['market']


class MarketTraceFilter(FilterSet):

    market = filters.CharFilter(field_name='market__id')

    class Meta:
        model = models.MarketTrace
        fields = ['market']
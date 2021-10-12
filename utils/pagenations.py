from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination


# 基础分页器
class MyPageNumberPagination(PageNumberPagination):

    # ?page=页码
    page_query_param = 'page'
    page_size = 50
    page_size_query_param = 'pageSize'
    max_page_size = 1000


# 偏移分页器
class MyLimitOffsetPagination(LimitOffsetPagination):
    # ?offset=从头偏移的条数&limit=要显示的条数
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    # ？不传offset和limit默认显示前3条，只设置offset就是从偏移位往后再显示3条
    default_limit = 3
    # ?limit可以自定义一页显示的最大条数
    max_limit = 5

    # 只使用limit结合ordering可以实现排行前几或后几
    #?ordering=price&limit=4 价格最低4个
    #?ordering=-price&limit=4 价格最高4个


# 游标分页器(加密)
# 注：必须基于排序规则下进行分页
# 1 如果接口配置了OrderingFilter过滤器，那么url中必须传ordering
# 2 如果接口没有配置OrderingFilter过滤器，一定要在分页类中声明ordering按某个字段进行默认
class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5
    ordering = '-pk'
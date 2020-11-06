from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from . import models, serializers, filters
from utils.response import APIResponse
from utils.authentications import JWTAuthentication
from utils.pagenations import MyPageNumberPagination

class ProductViewSet(ModelViewSet):

    queryset = models.Product.objects.all().order_by('id')
    serializer_class = serializers.ProductModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]

class ProductionViewSet(ModelViewSet):

    queryset = models.Production.objects.all().order_by('id')
    serializer_class = serializers.ProductionModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.ProductionFilterSet



#########
# 标签
########
class AisleViewSet(ModelViewSet):

    queryset = models.Aisle.objects.all()
    serializer_class = serializers.AisleModelSerializer


class PdStatusViewSet(ModelViewSet):

    queryset = models.ProductStatus.objects.all()
    serializer_class = serializers.PdStatusModelSerializer


class LifecycleViewSet(ModelViewSet):

    queryset = models.Lifecycle.objects.all()
    serializer_class = serializers.LifecycleModelSerializer
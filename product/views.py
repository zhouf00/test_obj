from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from . import models, serializers, filters
from engineering import models as e_models
from utils.response import APIResponse
from utils.pagenations import MyPageNumberPagination


class ProductViewSet(ModelViewSet):

    queryset = models.Product.objects.all().order_by('id')
    serializer_class = serializers.ProductModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]


class ProductListViewSet(ModelViewSet):

    queryset = models.Product.objects.all().order_by('id')
    serializer_class = serializers.ProductModelSerializer


class ProductionViewSet(ModelViewSet):

    queryset = models.Production.objects.all().order_by('id')
    serializer_class = serializers.ProductionModelSerializer

    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = filters.ProductionFilterSet

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.add_data(serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.add_data(serializer.data)
        return APIResponse(
            data_msg='list ok',
            results=serializer.data
        )

    def add_data(self, data):
        product_obj = models.Product.objects.all()
        productionStatus_obj = models.ProductionStatus.objects.all()
        project_obj = e_models.Project.objects.all()

        for var in data:
            var['projectName'] = project_obj.filter(id=var['project']).first().name
            var['productInfo'] = product_obj.filter(id=var['product']).values('title','hard_version').first()
            # var['statusName'] = productionStatus_obj.filter(id=var['status']).first().title
        pass


#########
# 标签
########
class AisleViewSet(ModelViewSet):

    queryset = models.Aisle.objects.all().order_by('sort')
    serializer_class = serializers.AisleModelSerializer


class PdStatusViewSet(ModelViewSet):

    queryset = models.ProductStatus.objects.all().order_by('sort')
    serializer_class = serializers.PdStatusModelSerializer


class LifecycleViewSet(ModelViewSet):

    queryset = models.Lifecycle.objects.all().order_by('sort')
    serializer_class = serializers.LifecycleModelSerializer


class ProductionStatusViewSet(ModelViewSet):

    queryset = models.ProductionStatus.objects.all().order_by('sort')
    serializer_class = serializers.ProductionStatusModelSerializer

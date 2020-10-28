import datetime
from rest_framework import serializers

from . import models
from personnel.serializers import UserModelSerializer


class ProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ['id', 'title', 'model', 'image', 'memo','status', 'aisle', 'hard_version',
                  'aisleInfo', 'statusInfo']

    def validate(self, attrs):
        print(attrs)
        return attrs


class ProductionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Production
        fields = ['id', 'sn', 'facility', 'sw', 'ip', 'memo', 'product', 'lifecycle', 'project',
                  'productInfo', 'lifecycleInfo']


#########
# 标签
########
class AisleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Aisle
        fields = '__all__'


class PdStatusModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductStatus
        fields = '__all__'


class LifecycleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lifecycle
        fields = '__all__'

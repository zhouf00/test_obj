import datetime
from rest_framework import serializers

from engineering import models
from personnel.serializers import UserModelSerializer


class MachineModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Machine
        fields = '__all__'


class ManufacturerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Manufacturer
        fields = '__all__'


class IdcRoomModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.IdcRoom
        fields = "__all__"

    def validate(self, attrs):
        print(attrs)
        return attrs


class CreateProjectModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = ['id', 'is_delete', 'name', 'address', 'sn', 'area', 'manufacturers', 'entrance_time','facility_count',
                  'status', 'monitor_type', 'type', 'builders', 'manager', 'working_env']

    def validate(self, attrs):
        sn = attrs['sn']
        if sn and models.Project.objects.filter(sn=sn):
            raise serializers.ValidationError({'msg': '该编号已经存在'})
        elif not sn:
            attrs.pop('sn')
        print(attrs)
        return attrs


class ProjectModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Project
        fields = ['id', 'is_delete', 'name', 'address', 'sn', 'update_time', 'entrance_time', 'finish_time',
                  'facility_count', 'manager', #'manufacturers', 'builders', 'facility', 'area',  'status',
                  'monitortypeList', 'typeInfo', 'statusInfo', 'areaInfo', 'working_envInfo', 'buildersList',
                  'manufacturersList']

        extra_kwargs = {
            'is_delete': {
              'write_only':True
            },
            'image': {
                'required': False
            },
            'entrance_time': {
                'required': False
            },
            'finish_time': {
                'required': False
            },
        }


class StockModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Stock
        fields = ['id', 'title', 'type', 'totality', 'delivered', 'undelivered', 'update_time', 'finish',
                  'project', 'typeInfo', 'finishInfo']


class InvoiceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Invoice
        fields = ['id', 'title', 'type', 'count', 'memo', 'project', 'user', 'create_time','img',
                  'userInfo']
        extra_kwargs = {
            'img': {
                'required': False
            },
        }


class InvoiceImageModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InvoiceImage
        fields = ['id', 'title', 'image', 'invoice']


######
# 标签组
#####
class MonitorTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonitorType
        fields = ['id', 'title']

class ProjectTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectType
        fields = ['id', 'title']


class ProjectStatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectStatus
        fields = ['id', 'title']


class ProjectAreaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectArea
        fields = ['id', 'title']


class ProjectWorkingEnvModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectWorkingEnv
        fields = ['id', 'title']


class StockFinishModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StockFinish
        fields = ['id', 'title']
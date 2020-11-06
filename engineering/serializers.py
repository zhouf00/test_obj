import datetime
from rest_framework import serializers

from engineering import models


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
        return attrs


class CreateProjectModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = ['id', 'is_delete', 'name', 'address', 'sn', 'area', 'manufacturers', 'entrance_time',
                  'facility_count', 'pj_sn','province', 'user_car','memo',
                  'status', 'monitor_type', 'type', 'builders', 'manager', 'working_env']

    def validate(self, attrs):
        # print(attrs)
        sn = attrs['sn']
        pj_sn = attrs['pj_sn']
        if self.instance:
            id = self.instance.id
        else:
            id = None
        if sn and len(sn) < 4:
            attrs['sn'] = sn.zfill(4)
        elif not sn:
            attrs.pop('sn')
        if sn and models.Project.objects.filter(sn=attrs['sn']).exclude(id=id):
            raise serializers.ValidationError({'msg': '该内部编号已经存在'})
        if pj_sn and models.Project.objects.filter(sn=pj_sn).exclude(id=id):
            raise serializers.ValidationError({'msg': '该项目编号已经存在'})
        return attrs


class ProjectModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Project
        fields = [
            'id', 'is_delete', 'name', 'address', 'sn', 'update_time', 'entrance_time', 'finish_time',
            'facility_count', 'manager', 'memo', 'pj_sn',
            # 自定义信息
            'monitortypeList', 'typeInfo', 'statusInfo', 'areaInfo', 'working_envInfo', 'buildersList',
             'manufacturersList', 'monitorNumberList'
        ]

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


class ProjectTraceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectTrace
        fields = ['create_time', 'content', 'user', 'project', 'userInfo']


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


class MonitorNumberModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonitorNumber
        fields = ['id', 'project', 'title', 'number']



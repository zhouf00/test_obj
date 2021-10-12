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


# 项目的序列化
class ProjectModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = models.Project
        fields = [
            'id', 'is_delete', 'name', 'address', 'sn', 'update_time', 'entrance_time', 'finish_time', 'begin_time', 'check_time',
            'facility_count', 'manager', 'memo', 'pj_sn', 'stock_finish', 'product', 'manufacturers','priority','serial',
            'type', 'province', 'monitor_type', 'area', 'working_env', 'diagnosisman', 'salesman', 'builders', 'collect',
            'out_warranty','submitter', 'priority2', 'FAEman',
            # 自定义信息
            'monitortypeList', 'typeInfo', 'statusInfo', 'areaInfo', 'working_envInfo', 'manufacturersList',
            'monitorNumberList', 'diagnosismanList', 'buildersList', 'priorityInfo', 'trace_statusInfo'
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
            'product': {
                'required': False
            }
        }


class ProjectListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['id', 'name', 'serial', 'status','builders', 'manager', 'contract']


# 项目删除的序列化
class ProjectDeleteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['id', 'is_delete']


class FacilityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Facility
        fields = '__all__'


# 项目时间轴
class ProjectStatusTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectStatusTime
        fields = ['id', 'status', 'time', 'user', 'project', 'info']


# 承包信息序列化
class ContractModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Contract
        fields = ['id', 'project', 'name', 'context', 'payment', 'payment_rate', 'delivery_time',
                  'payment_time','nameInfo', 'submitter']


# 承包付款信息
class PaymentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Payment
        fields = '__all__'


# 承包商序列化
class OutsourcerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Outsourcer
        fields = ['id', 'type', 'title', 'scale', 'linkman', 'phone', 'join_time', 'memo']


class StockModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Stock
        fields = ['id', 'title', 'type', 'totality', 'delivered', 'undelivered', 'update_time', 'finish',
                  'project', 'typeInfo', 'finishInfo']


class InvoiceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Invoice
        fields = ['id', 'title', 'type', 'count', 'memo', 'project', 'user', 'create_time','img',
                  'invoice_time',
                  'userInfo']
        extra_kwargs = {
            'img': {
                'required': False
            },
        }


# 临时修改时间
class InvoiceUpdateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Invoice
        fields = ['id', 'invoice_time']


class InvoiceImageModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.InvoiceImage
        fields = ['id', 'title', 'image', 'invoice']


class ProjectTraceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectTrace
        fields = '__all__'
        # fields = ['id', 'is_delete', 'create_time', 'update_time', 'status','outsourcer', 'project', 'user', 'worklog',
        #           'task', 'subscriber']


# 项目修改更新时间
class ProjectUpdateTime(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = ['id', 'priority', 'stock_finish']


class ProjectCollect(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ['id', 'collect']


######
# 标签组
#####
class ProjectPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectPriority
        fields = '__all__'


class ProjectPriority2Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectPrority2
        fields = '__all__'


class MonitorTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonitorType
        fields = '__all__'


class ProjectTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectType
        fields = '__all__'


class ProjectStatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectStatus
        fields = '__all__'


class ProjectAreaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectArea
        fields = '__all__'


class ProjectWorkingEnvModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectWorkingEnv
        fields = '__all__'


class StockFinishModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StockFinish
        fields = '__all__'


class MonitorNumberModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonitorNumber
        fields = ['id', 'project', 'title', 'number']


class TraceStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TraceStatus
        fields = '__all__'

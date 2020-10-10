import datetime
from rest_framework import serializers

from engineering import models
from personnel.serializers import UserModelSerializer


class ManufacturerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Manufacturer
        fields = '__all__'


class CreateProjectModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = ['id', 'is_delete', 'name', 'address', 'sn', 'area', 'manufacturers', 'entrance_time',
                  'status', 'priority', 'monitor_type', 'type', 'builders']

    def validate(self, attrs):
        print(attrs)
        return attrs


class CpuModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CPU
        fields = '__all__'


class RamModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RAM
        fields = '__all__'


class DiskModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Disk
        fields = '__all__'


class NicModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NIC
        fields = '__all__'


class ServerModelSerializer(serializers.ModelSerializer):

    cpu = CpuModelSerializer(many=False, read_only=True)
    ram = RamModelSerializer(many=True, read_only=True)
    disk = DiskModelSerializer(many=True, read_only=True)
    nic = NicModelSerializer(many=True, read_only=True)

    class Meta:
        model = models.Server
        fields = ['id', 'is_delete', 'server_type', 'brand', 'model', 'os_type', 'os_release',
                  'accounts', 'passwd', 'place', 'project',
                  'cpu', 'ram', 'disk', 'nic']


class CollectorModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Collector
        fields = '__all__'


class SensorModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sensor
        fields = '__all__'


class FacilitySensorModelSerializer(serializers.ModelSerializer):

    sensor_type = SensorModelSerializer(many=False, read_only=True)

    class Meta:
        model = models.FacilitySensor
        fields = '__all__'


class FacilityCollectorModelSerializer(serializers.ModelSerializer):

    sensor = FacilitySensorModelSerializer(many=True, read_only=True)
    collector_type = CollectorModelSerializer(many=False, read_only=True)

    class Meta:
        model = models.FacilityCollector
        fields = '__all__'


class MachineModelSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerModelSerializer(many=False, read_only=True)

    class Meta:
        model = models.Machine
        fields = '__all__'


class MonitorTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonitorType
        fields = ['id', 'title']


class FacilityModelSerializer(serializers.ModelSerializer):
    """设备"""
    collector = FacilityCollectorModelSerializer(many=True, read_only=True)
    machine = MachineModelSerializer(many=False, read_only=True)

    class Meta:
        model = models.Facility
        fields = '__all__'


class ProjectModelSerializer(serializers.ModelSerializer):

    manufacturers = ManufacturerModelSerializer(many=True)
    builders = UserModelSerializer(many=True)
    facility = FacilityModelSerializer(many=True)
    monitor_type = MonitorTypeModelSerializer(many=True)

    class Meta:
        model = models.Project
        fields = ['id', 'is_delete', 'name', 'area', 'priority', 'address', 'sn', 'status',
                  'update_time', 'entrance_time', 'finish_time', 'facility_count',
                  'manufacturers', 'builders', 'facility', 'server', 'monitor_type']

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


class DetailModelSerializer(serializers.ModelSerializer):

    # 引入其它序列化数据
    server = ServerModelSerializer(many=True, read_only=True)
    facility = FacilityModelSerializer(many=True, read_only=True)

    # 重写to_representation方法，进行数据的过滤
    def to_representation(self, obj):
        data = super(DetailModelSerializer, self).to_representation(obj)
        data['server'] = self._filter(
            ServerModelSerializer,
            models.Server.objects.filter(is_delete=False, project=obj.id)
        )
        data['facility'] = self._filter(
            FacilityModelSerializer,
            models.Facility.objects.filter(is_delete=False, project=obj.id)
        )
        return data

    class Meta:
        model = models.Project
        fields = ['id', 'create_time', 'name', 'is_delete', 'address', 'sn', 'status', 'image', 'memo',
                   'server', 'facility', 'manu_list']

    # 自定义过滤方法
    def _filter(self, ser, obj):
        temp_list = []
        for var in obj:
            temp_list.append(ser(var).data)
        return temp_list
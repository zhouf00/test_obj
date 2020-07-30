from rest_framework import serializers

from engineering import models


class ProjectModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = ['id', 'is_delete', 'name', 'address', 'sn', 'status', 'manu_list']

        extra_kwargs = {
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


class ServerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Server
        fields = ['id', 'is_delete', 'server_type', 'brand', 'model', 'os_type', 'os_release',
                  'accounts', 'passwd', 'place', 'project',
                  'cpu_list', 'ram_list', 'disk_list', 'nic_list']


class CollectorModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Collector
        fields = '__all__'


class SensorModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Sensor
        fields = '__all__'


class FacilitySensorModelSerializer(serializers.ModelSerializer):

    sensor_type = SensorModelSerializer(many=False)

    class Meta:
        model = models.FacilitySensor
        fields = '__all__'


class FacilityCollectorModelSerializer(serializers.ModelSerializer):

    sensor = FacilitySensorModelSerializer(many=True)
    collector_type = CollectorModelSerializer(many=False)

    class Meta:
        model = models.FacilityCollector
        fields = '__all__'


class ManufacturerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Manufacturer
        fields = '__all__'


class MachineModelSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerModelSerializer(many=False)

    class Meta:
        model = models.Machine
        fields = '__all__'


class FacilityModelSerializer(serializers.ModelSerializer):
    """设备"""
    collector = FacilityCollectorModelSerializer(many=True)
    machine = MachineModelSerializer(many=False)

    class Meta:
        model = models.Facility
        fields = '__all__'


class DetailModelSerializer(serializers.ModelSerializer):

    # 引入其它序列化数据
    server = ServerModelSerializer(many=True)
    facility = FacilityModelSerializer(many=True)

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
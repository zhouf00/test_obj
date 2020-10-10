from django.db import models


from utils.basemodel import BaseModel, upload_path_image
# Create your models here.


class Project(BaseModel):

    type = models.CharField(max_length=16, verbose_name='项目类型')
    name = models.CharField(max_length=64, unique=True, verbose_name='项目名称')
    area = models.CharField(max_length=32, blank=True, null=True,  verbose_name='区域')
    priority = models.SmallIntegerField(default=1, verbose_name='优先级')
    address = models.CharField(max_length=64, verbose_name='项目地址')
    sn = models.CharField(max_length=64, unique=True, verbose_name='内部项目编号')
    status = models.SmallIntegerField(default=1, verbose_name='项目状态')
    facility_count = models.IntegerField(default=0, verbose_name='设备数量')

    image = models.ImageField(upload_to=upload_path_image, default='img/default.jpg', blank=True, null=True, verbose_name='默认图片')
    entrance_time = models.DateTimeField(blank=True, null=True, verbose_name='入场时间')
    finish_time = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    memo = models.TextField(blank=True, null=True, verbose_name='备注说明')

    # x = models.DecimalField(max_digits=10, decimal_places=5)

    manufacturers = models.ManyToManyField(
        to='Manufacturer',
        db_constraint=False,
        related_name='project'
    )

    monitor_type = models.ManyToManyField(
        to='MonitorType',
        db_constraint=False,
        related_name='project'
    )

    # builders = models.ManyToManyField(
    #     to='personnel.User',
    #     db_constraint=False,
    #     related_name='project'
    # )

    def __str__(self):
        return '%s'%(self.name)

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name


class Server(BaseModel):
    # 添加供应商联系方式
    SERVER_TYPE_CHOICE = (
        (0, '塔式服务器'),
        (1, '柜式服务器'),
        (2, 'PC电脑'),
    )
    OS_TYPE_CHOICE = (
        (1, 'Windows'),
        (2, 'linux')
    )
    DISK_RAID_CHOICE = (
        (1, 'RAID 0'),
        (2, 'RAID 1'),
        (3, 'RAID 5')
    )

    project = models.ForeignKey(to='Project', related_name='server', on_delete=models.CASCADE)
    server_type = models.CharField(max_length=32, verbose_name='服务器类型')
    brand = models.CharField(max_length=32, verbose_name='品牌')
    model = models.CharField(max_length=64, verbose_name='服务器型号')
    os_type = models.CharField(max_length=32, blank=True, null=True,  verbose_name='系统类型')
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name='系统版本')
    place = models.CharField(max_length=64, blank=True, null=True, verbose_name='存放位置')
    accounts = models.CharField(max_length=32, blank=True, null=True, verbose_name='帐号')
    passwd = models.CharField(max_length=32, blank=True, null=True, verbose_name='密码')
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return '%s %s%s'%(self.project.name, self.brand, self.model)

    class Meta:
        verbose_name = '风场服务器'
        verbose_name_plural = verbose_name


class CPU(BaseModel):

    server = models.OneToOneField(to='Server', on_delete=models.CASCADE, related_name='cpu')
    cpu_model = models.CharField(max_length=128, blank=True, null=True, verbose_name='CPU型号')
    cpu_core_count = models.SmallIntegerField(default=4, blank=True, null=True, verbose_name='CPU核心数')
    cpu_count = models.SmallIntegerField(default=1, blank=True, null=True, verbose_name='CPU物理个数')

    def __str__(self):
        return '%s(%s核心)*%s'%(self.cpu_model, self.cpu_core_count, self.cpu_count)

    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = verbose_name


class RAM(BaseModel):

    server = models.ForeignKey(to='Server', on_delete=models.CASCADE, related_name='ram')
    capacity = models.IntegerField(default=8, blank=True, null=True, verbose_name='内存大小')
    ram_count = models.SmallIntegerField(default=1, blank=True, null=True, verbose_name='内存数量')

    def __str__(self):
        return '%sGB'%self.capacity

    class Meta:
        verbose_name = '内存'
        verbose_name_plural = verbose_name


class Disk(BaseModel):

    server = models.ForeignKey(to='Server', on_delete=models.CASCADE, related_name='disk')
    disk_type = models.CharField(max_length=16, verbose_name='硬件类型')
    disk_capacity = models.FloatField(verbose_name='硬盘容量(GB)')
    disk_count = models.SmallIntegerField(default=2, blank=True, null=True, verbose_name='硬盘数量')
    disk_raid = models.CharField(max_length=16, blank=True, null=True, verbose_name='阵列类型')

    def __str__(self):
        return '%s %sGB'%(self.disk_type, self.disk_capacity)

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = verbose_name


class NIC(BaseModel):

    server = models.ForeignKey(to='Server', on_delete=models.CASCADE, related_name='nic')
    title = models.CharField(max_length=64, blank=True, null=True, verbose_name='网卡名称')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')
    net_mask = models.GenericIPAddressField(blank=True, null=True, verbose_name='子网掩码')
    gate_way = models.GenericIPAddressField(blank=True, null=True, verbose_name='网关')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return '%s %s'%(self.title, self.ip_address)

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = verbose_name


class Facility(BaseModel):

    project = models.ForeignKey(
        to='Project',
        on_delete=models.CASCADE,
        related_name='facility'
    )

    title = models.CharField(max_length=64, verbose_name='风机名称')
    status = models.SmallIntegerField(default=1, blank=True, null=True, verbose_name='风机运行状态')
    memo = models.TextField(verbose_name='备注')

    machine = models.ForeignKey(
        to='Machine',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '%s %s(%s)'%(self.project.name, self.title, self.machine.title)

    class Meta:
        verbose_name = '项目风机'
        verbose_name_plural = verbose_name


class Machine(BaseModel):

    title = models.CharField(max_length=64, verbose_name='机器型号')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    manufacturer = models.ForeignKey(
        to='Manufacturer',
        on_delete=models.CASCADE,
        related_name='machine'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '设备型号'
        verbose_name_plural = verbose_name


class Manufacturer(BaseModel):

    title = models.CharField(max_length=64, verbose_name='厂商名称')
    telephone = models.CharField(max_length=11, blank=True, null=True, verbose_name='厂商电话')
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = verbose_name


class FacilityCollector(BaseModel):

    facility = models.ForeignKey(
        to='Facility',
        on_delete=models.CASCADE,
        related_name='collector'
    )

    sn = models.CharField(max_length=64, verbose_name='采集器编号')
    types = models.SmallIntegerField(default=1, blank=True, null=True, verbose_name='采集类型')
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    net_mask = models.GenericIPAddressField(null=True, blank=True, verbose_name='子网掩码')
    gate_way = models.GenericIPAddressField(null=True, blank=True, verbose_name='网关')
    model = models.CharField(max_length=64, verbose_name='目前版本')

    collector_type = models.ForeignKey(
        to='Collector',
        on_delete=models.CASCADE,
        related_name='facility_collector'
    )

    def __str__(self):
        return '%s %s(%s)'%(self.facility.title, self.types, self.sn)

    class Meta:
        verbose_name = '风机采集器'
        verbose_name_plural = verbose_name


class FacilitySensor(BaseModel):

    collector = models.ForeignKey(
        to='FacilityCollector',
        on_delete=models.CASCADE,
        related_name='sensor'
    )
    sn = models.CharField(max_length=64, verbose_name='采集器编号')
    number = models.SmallIntegerField(default=1, verbose_name='通道编号')
    install_site = models.CharField(max_length=64, null=True, blank=True, verbose_name='安装位置')
    sensor_type = models.ForeignKey(
        to='Sensor',
        on_delete=models.CASCADE,
        related_name='facility_sensor'
    )

    def __str__(self):
        return '%s<%s>%s'%(self.collector, self.number, self.sensor_type.title)

    class Meta:
        verbose_name = '风机传感器'
        verbose_name_plural = verbose_name


class Stock(BaseModel):
    pass


class EventLog(BaseModel):

    project = models.ForeignKey(to='Project', on_delete=models.CASCADE, related_name='log')
    event_type = models.SmallIntegerField(default=1, verbose_name='事件类型')
    date = models.DateTimeField(auto_now_add=True, verbose_name='事件时间')
    detail = models.TextField(verbose_name='事件详情')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '日志'
        verbose_name_plural = verbose_name


class Collector(BaseModel):
    """公司物料-采集器"""

    title = models.CharField(max_length=64, verbose_name='采集器名称')
    model = models.CharField(max_length=64, verbose_name='版本')
    aisle = models.IntegerField(verbose_name='通道数量')
    image = models.ImageField(blank=True, null=True, verbose_name='采集器照片')
    memo = models.TextField(verbose_name='备注')

    def __str__(self):
        return '%s %s(%s)'%(self.title, self.model, self.aisle)

    class Meta:
        verbose_name = '采集器'
        verbose_name_plural = verbose_name


class Sensor(BaseModel):
    """公司物料-传感器"""

    title = models.CharField(max_length=64, verbose_name='传感器名称')
    bias_voltage = models.CharField(max_length=32, null=True, blank=True, verbose_name='偏置电压')
    memo = models.TextField(verbose_name='备注')

    manufacturer = models.ForeignKey(
        to='Manufacturer',
        on_delete=models.CASCADE,
        related_name='sensor'
    )

    def __str__(self):
        return '%s(%s)'%(self.title, self.bias_voltage)

    class Meta:
        verbose_name = '传感器'
        verbose_name_plural = verbose_name


class MonitorType(BaseModel):

    title = models.CharField(max_length=64, verbose_name='监测名称')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '监测类型'
        verbose_name_plural = verbose_name
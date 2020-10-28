from django.db import models

from utils.basemodel import BaseModel, upload_path_image


# 项目
class Project(BaseModel):

    name = models.CharField(max_length=64, unique=True, verbose_name='项目名称')
    priority = models.SmallIntegerField(default=1, verbose_name='优先级')
    address = models.CharField(max_length=64, verbose_name='项目地址')
    sn = models.CharField(max_length=64, blank=True, null=True, verbose_name='内部项目编号')
    facility_count = models.IntegerField(default=0, verbose_name='设备数量')
    contractor = models.CharField(max_length=64, blank=True, null=True, verbose_name='承包商')
    manager = models.CharField(max_length=64, blank=True, null=True, verbose_name='项目负责人')

    image = models.ImageField(upload_to=upload_path_image, default='img/default.jpg', blank=True, null=True,
                              verbose_name='默认图片')
    entrance_time = models.DateTimeField(blank=True, null=True, verbose_name='入场时间')
    finish_time = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    memo = models.TextField(blank=True, null=True, verbose_name='备注说明')

    # 坐标待使用
    # x = models.DecimalField(max_digits=10, decimal_places=5)

    type = models.ForeignKey(
        to='ProjectType',
        on_delete=models.CASCADE,
        related_name='project',
        verbose_name='项目类型',
        blank=True, null=True
    )
    status = models.ForeignKey(
        to='ProjectStatus',
        on_delete=models.CASCADE,
        related_name='project',
        verbose_name='项目状态',
        blank=True, null=True
    )
    area = models.ForeignKey(
        to='ProjectArea',
        on_delete=models.CASCADE,
        related_name='project',
        verbose_name='项目区域',
        blank=True, null=True
    )
    working_env = models.ForeignKey(
        to='ProjectWorkingEnv',
        on_delete=models.CASCADE,
        related_name='project',
        verbose_name='项目作业环境',
        blank=True, null=True
    )
    manufacturers = models.ManyToManyField(
        to='Manufacturer',
        db_constraint=False,
        related_name='project'
    )

    @property
    def monitortypeList(self):
        return self.monitor_type.values('id', 'title')

    @property
    def buildersList(self):
        return self.builders.values('id','name')

    @property
    def manufacturersList(self):
        return self.manufacturers.values('id', 'title')

    @property
    def typeInfo(self):
        return self.type.info

    @property
    def areaInfo(self):
        return self.area.info

    @property
    def statusInfo(self):
        return self.status.info

    @property
    def working_envInfo(self):
        return self.working_env.info

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name


# 机房设备
class IdcRoom(BaseModel):

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='idcroom')
    title = models.CharField(max_length=32, verbose_name='设备名称')
    sn = models.CharField(max_length=64, blank=True, null=True, verbose_name='SN号或快速服务代码')
    describe = models.TextField(verbose_name='设备描述')
    software = models.CharField(blank=True, null=True, max_length=32, verbose_name='安装软件版本')
    ip = models.TextField(blank=True, null=True, verbose_name='ip信息')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '机房信息'
        verbose_name_plural = verbose_name


# 设备型号
class Machine(BaseModel):
    title = models.CharField(max_length=64, verbose_name='机器型号')
    param = models.TextField(blank=True, null=True, verbose_name='设备参数')
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


# 厂家
class Manufacturer(BaseModel):
    title = models.CharField(max_length=64, verbose_name='厂商名称')
    telephone = models.CharField(max_length=11, blank=True, null=True, verbose_name='厂商电话')
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = verbose_name


class Stock(BaseModel):

    project = models.ForeignKey(
        to='Project', on_delete=models.CASCADE, related_name='stock',
        blank=True, null=True
    )

    title = models.CharField(max_length=32, verbose_name='货物名称')
    type = models.ForeignKey(
        'engineering.MonitorType', on_delete=models.CASCADE, verbose_name='货物类型',
        blank=True, null=True,
    )
    totality = models.IntegerField(blank=True, null=True, verbose_name='货物总数')
    delivered = models.IntegerField(blank=True, null=True, default=0, verbose_name='已发货')
    undelivered = models.IntegerField(blank=True, null=True, default=0, verbose_name='未发货')
    finish = models.ForeignKey(
        to="StockFinish", on_delete=models.CASCADE, verbose_name='是否完成',
        blank=True, null=True,
    )

    @property
    def typeInfo(self):
        return self.type.info

    @property
    def finishInfo(self):
        return self.finish.info

    class Meta:
        verbose_name = '库存管理'
        verbose_name_plural = verbose_name


class Invoice(BaseModel):

    project = models.ForeignKey(
        to='Project', on_delete=models.CASCADE, related_name='invoice',
        blank=True, null=True
    )
    title = models.CharField(max_length=32, verbose_name='货物名称')
    type = models.CharField(max_length=32,blank=True, null=True,  verbose_name='发货类型')
    count = models.IntegerField(blank=True, null=True, verbose_name='发货数量')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    user = models.ForeignKey('personnel.User', on_delete=models.CASCADE, verbose_name='发货人')

    @property
    def userInfo(self):
        return self.user.info

    class Meta:
        verbose_name = '发货清单'
        verbose_name_plural = verbose_name


class InvoiceImage(models.Model):

    title = models.CharField(max_length=64, blank=True, null=True, verbose_name='文件名称')
    image = models.ImageField(upload_to=upload_path_image, blank=True, null=True,
                              verbose_name='图片')
    invoice = models.ForeignKey(
        to='Invoice',
        on_delete=models.CASCADE,
        related_name='img',
        blank=True, null=True
    )

    class Meta:
        verbose_name = '发货图片'
        verbose_name_plural = verbose_name


class EventLog(BaseModel):
    project = models.ForeignKey(to='Project', on_delete=models.CASCADE, related_name='log')
    event_type = models.SmallIntegerField(default=1, verbose_name='事件类型')
    detail = models.TextField(verbose_name='事件详情')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')



    class Meta:
        verbose_name = '日志'
        verbose_name_plural = verbose_name



##########
# 标签模型
##########
class MonitorType(models.Model):

    project = models.ManyToManyField(
        to='Project',
        db_constraint=False,
        related_name='monitor_type',
        blank=True
    )
    title = models.CharField(max_length=64, verbose_name='监测名称')

    @property
    def info(self):
        var = {
            'id': self.id,
            'title': self.title,
        }
        return var

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '监测类型'
        verbose_name_plural = verbose_name


class ProjectWorkingEnv(models.Model):

    title = models.CharField(max_length=64, verbose_name='环境名称')

    @property
    def info(self):
        var = {
            'id': self.id,
            'title': self.title,
        }
        return var

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '作业环境'
        verbose_name_plural = verbose_name


class ProjectStatus(models.Model):

    title = models.CharField(max_length=64, verbose_name='状态名称')

    @property
    def info(self):
        var = {
            'id': self.id,
            'title': self.title,
        }
        return var

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '项目状态'
        verbose_name_plural = verbose_name


class ProjectArea(models.Model):

    title = models.CharField(max_length=64, verbose_name='区域名称')

    @property
    def info(self):
        var = {
            'id': self.id,
            'title': self.title,
        }
        return var

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '区域信息'
        verbose_name_plural = verbose_name


class ProjectType(models.Model):

    title = models.CharField(max_length=64, verbose_name='项目类型')

    @property
    def info(self):
        var = {
            'id': self.id,
            'title': self.title,
        }
        return var

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '项目类型'
        verbose_name_plural = verbose_name


class StockFinish(models.Model):

    title = models.CharField(max_length=64, verbose_name='标签')

    @property
    def info(self):
        var = {
            'id': self.id,
            'title': self.title,
        }
        return var

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '库存完成与否'
        verbose_name_plural = verbose_name

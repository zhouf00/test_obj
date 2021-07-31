from django.db import models

from utils.basemodel import BaseModel, upload_path_image


# 产品管理
class Product(BaseModel):
    """公司产品-采集器"""

    title = models.CharField(max_length=64, verbose_name='采集器名称')
    model = models.CharField(max_length=64, verbose_name='型号')
    hard_version = models.CharField(max_length=64, verbose_name='硬件版本')
    image = models.ImageField(blank=True, null=True, verbose_name='采集器照片')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    status = models.ForeignKey(
        to='ProductStatus',
        on_delete=models.CASCADE,
        related_name='product',
        blank=True, null=True,
    )

    aisle = models.ForeignKey(
        to='Aisle',
        on_delete=models.CASCADE,
        related_name='product',
        blank=True, null=True,
    )

    @property
    def aisleInfo(self):
        return self.aisle.info if self.aisle else {}

    @property
    def statusInfo(self):
        return self.status.info

    @property
    def info(self):
        return {
            'id': self.id,
            'title': self.title,
            'model': self.model,
            'hard_version': self.hard_version,
            'memo': self.memo,
            'aisleTitle': self.aisleInfo
        }

    def __str__(self):
        return '%s %s(%s)' % (self.title, self.model, self.aisle)

    class Meta:
        verbose_name = '公司产品'
        verbose_name_plural = verbose_name


# 生产出的产品
class Production(BaseModel):

    project = models.ForeignKey(
        'engineering.Project',
        on_delete=models.CASCADE,
        related_name='production',
        blank=True, null=True,)
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='production')
    sn = models.CharField(max_length=32, blank=True, null=True, verbose_name='产品编号')
    facility = models.CharField(max_length=64, blank=True, null=True, verbose_name='绑定设备')
    sw = models.CharField(max_length=32, blank=True, null=True, verbose_name='嵌入式版本')
    ip = models.TextField(blank=True, null=True, verbose_name='采集器IP')
    # sensor = models.TextField(blank=True, null=True, verbose_name='传感器')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    lifecycle = models.ForeignKey(
        'Lifecycle', on_delete=models.CASCADE, related_name='production',
        blank=True, null=True,
    )

    @property
    def productInfo(self):
        return self.product.info if self.product else {}

    @property
    def lifecycleInfo(self):
        return self.lifecycle.info

    def __str__(self):
        return '%s %s'% (self.sn, self.product.model)

    class Meta:
        verbose_name = '生产出的采集器'
        verbose_name_plural = verbose_name


# 产品日志
class ProductionLog(BaseModel):

    issue_status = models.CharField(blank=True, null=True,
        max_length=64, verbose_name='问题状态')
    title = models.CharField(blank=True, null=True,
        max_length=64, verbose_name='操作信息')    # 生产、维修、安装、返修、发货
    content = models.TextField(blank=True, null=True,
        verbose_name='正文')
    user = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(User) 提交人')
    production = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(Production) 设备')
    project = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(Project) 设备')
    # production = models.ForeignKey(
    #     'Production', on_delete=models.CASCADE, related_name='productionlog',
    #     blank=True, null=True,
    #     verbose_name='关联-(Production) 产品')
    facility = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(Facility) 设备')
    worklog = models.SmallIntegerField(blank=True, null=True,
                                       verbose_name='日志汇报')
    subscriber = models.ManyToManyField(
        to='personnel.User',
        db_constraint=False,
        related_name='ProductionLog_sub',
        blank=True,
        verbose_name='参与者'
    )


#########
# 标签
########
class ProductStatus(models.Model):
    title = models.CharField(max_length=32, verbose_name='产品编号')

    @property
    def info(self):
        return {
            'id': self.id,
            'title':self.title
        }

    class Meta:
        verbose_name = '产品使用状态'
        verbose_name_plural = verbose_name


class ProductionStatus(models.Model):
    title = models.CharField(max_length=32, verbose_name='出产产品状态')

    @property
    def info(self):
        return {
            'id': self.id,
            'title':self.title
        }

    class Meta:
        verbose_name = '出产产品状态'
        verbose_name_plural = verbose_name


class Lifecycle(models.Model):

    title = models.CharField(max_length=32, verbose_name='产品编号')

    @property
    def info(self):
        return {
            'id': self.id,
            'title':self.title
        }

    class Meta:
        verbose_name = '生命周期'
        verbose_name_plural = verbose_name


class Aisle(models.Model):
    """采集器通道类型"""
    title = models.CharField(max_length=64, verbose_name='通道名称')
    count = models.IntegerField(blank=True, null=True, verbose_name='通道数量')

    @property
    def info(self):
        var = {
            'id': self.id,
            'title': self.title,
            'count': self.count
        }
        return var

    class Meta:
        verbose_name = '通道信息'
        verbose_name_plural = verbose_name

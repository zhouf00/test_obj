from django.db import models

from personnel import models as p_models
from utils.basemodel import BaseModel
# Create your models here.


class Market(BaseModel):

    title = models.CharField(max_length=64, verbose_name='商机名称')
    # 类别是否需要独立建表
    customer = models.CharField(max_length=64, blank=True, null=True, verbose_name='客户名称')
    company = models.CharField(max_length=64, blank=True, null=True, verbose_name='集团公司')
    address = models.CharField(max_length=128, blank=True, null=True, verbose_name='地区')
    designing_institute = models.CharField(max_length=64, blank=True, null=True, verbose_name='设计院')
    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name='制造厂')
    sn = models.CharField(max_length=32, blank=True, null=True, verbose_name='编号')
    count = models.IntegerField(blank=True, null=True, verbose_name='设置数量')
    estimated_time = models.DateTimeField(blank=True, null=True, verbose_name='预计时间')
    estimated_amount = models.FloatField(default=0, blank=True, null=True, verbose_name='预额')
    hit_rate = models.FloatField(default=0, blank=True, null=True, verbose_name='命中率')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    traceTime = models.DateTimeField(blank=True, null=True, verbose_name='跟进时间')
    amount = models.FloatField(default=0, blank=True, null=True, verbose_name='漏额')

    # 天数
    days = 0

    type = models.ManyToManyField(
        to='product.Product',
        db_constraint=False,
        related_name='market'
    )

    user = models.ForeignKey(
        to='personnel.User',
        on_delete=models.CASCADE,
        related_name='market',
        blank=True, null=True
    )

    coadjutant = models.ManyToManyField(
        to='personnel.User',
        db_constraint=False,
        related_name='market_co',
        blank=True
    )

    @property
    def typeList(self):
        return self.type.values('id', 'title')

    @property
    def totalDays(self):
        return self.days

    @property
    def raterecordList(self):
        d = self.record.values('hit_rate', 'start_time', 'end_time', 'days').order_by('hit_rate')
        self.days=0
        for var in d:
           self.days += var['days']
        return d

    @property
    def userInfo(self):
        return self.user.info

    class Meta:
        verbose_name = '商机信息表'
        verbose_name_plural = verbose_name


class MarketTrace(BaseModel):

    hit_rate = models.FloatField(verbose_name='命中率')
    content = models.TextField(verbose_name='内容')

    market = models.ForeignKey(
        to='Market', on_delete=models.CASCADE, related_name='markettrace',
    )

    user = models.ForeignKey(
        to='personnel.User', on_delete=models.CASCADE, related_name='markettrace',
    )

    @property
    def userInfo(self):
        return self.user.info

    class Meta:
        verbose_name = '商机跟踪情况'
        verbose_name_plural = verbose_name


class Linkman(BaseModel):

    name = models.CharField(max_length=32, verbose_name='联系人名字')
    identity = models.CharField(max_length=32,blank=True, null=True,  verbose_name='身份')
    duty = models.CharField(max_length=32,blank=True, null=True,  verbose_name='职务')
    phone = models.CharField(max_length=11,blank=True, null=True,  verbose_name='手机')
    wechat = models.CharField(max_length=64, blank=True, null=True, verbose_name='微信')
    mail = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    market = models.ForeignKey(
        to='Market', on_delete=models.CASCADE, related_name='linkman',
    )

    class Meta:
        verbose_name = '商机联系人'
        verbose_name_plural = verbose_name


class RateRecord(models.Model):

    start_time = models.DateTimeField(blank=True, null=True,verbose_name='开始时间')
    end_time = models.DateTimeField(blank=True, null=True,verbose_name='结束时间')
    hit_rate = models.FloatField(verbose_name='命中率')
    days = models.SmallIntegerField(default=0, blank=True, null=True, verbose_name='天数')

    market = models.ForeignKey('Market', on_delete=models.CASCADE, related_name='record',
                              blank=True, null=True, verbose_name='命中率记录')

    class Meta:
        verbose_name = '命中率过程记录'
        verbose_name_plural = verbose_name


class MarketHistory(models.Model):

    estimated_amount = models.FloatField(default=0, blank=True, null=True, verbose_name='预额')
    amount = models.FloatField(default=0, blank=True, null=True, verbose_name='漏额')
    rate_0 = models.FloatField(default=0, blank=True, null=True, verbose_name='0%预额')
    rate_0_t = models.SmallIntegerField(default=0, blank=True, null=True, verbose_name='0%个数')
    rate_025 = models.FloatField(default=0, blank=True, null=True, verbose_name='25%预额')
    rate_025_t = models.SmallIntegerField(default=0, blank=True, null=True, verbose_name='25%个数')
    rate_050 = models.FloatField(default=0, blank=True, null=True, verbose_name='50%预额')
    rate_050_t = models.SmallIntegerField(default=0, blank=True, null=True, verbose_name='50%个数')
    rate_075 = models.FloatField(default=0, blank=True, null=True, verbose_name='75%预额')
    rate_075_t = models.SmallIntegerField(default=0, blank=True, null=True, verbose_name='75%个数')
    rate_100 = models.FloatField(default=0, blank=True, null=True, verbose_name='100%预额')
    rate_100_t = models.SmallIntegerField(default=0, blank=True, null=True, verbose_name='100%个数')
    date = models.DateTimeField(blank=True, null=True, verbose_name='日期')

    user = models.ForeignKey(
        to='personnel.User',
        on_delete=models.CASCADE,
        related_name='markethistory',
        blank=True, null=True
    )

    class Meta:
        verbose_name = '月历史记录'
        verbose_name_plural = verbose_name
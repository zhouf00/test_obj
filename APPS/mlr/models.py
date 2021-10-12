from django.db import models

from utils.basemodel import BaseModel, upload_path_file


# 任务单
class Task(BaseModel):


    status = models.SmallIntegerField(default=0, verbose_name='状态')
    priority = models.SmallIntegerField(default=0, verbose_name='来源')
    bagin_time = models.DateTimeField(blank=True, null=True,
                                      verbose_name='开始时间')
    end_time = models.DateTimeField(blank=True, null=True,
                                    verbose_name='结束时间')
    finish_time = models.DateTimeField(blank=True, null=True,
                                    verbose_name='完成时间')
    count = models.SmallIntegerField(verbose_name='任务数量')
    progress = models.SmallIntegerField(default=0,verbose_name='已完成数量')
    title = models.CharField(max_length=64, verbose_name='任务名称')
    content = models.TextField(blank=True, null=True, verbose_name='任务正文')

    submitter = models.SmallIntegerField(verbose_name='关联-(user) 提交人')

    executor = models.ManyToManyField(to='personnel.User',
        db_constraint=False,
        related_name='Task_exe',
        blank=True,
        verbose_name='关联-(user) 执行人'
                                        )
    subscriber = models.ManyToManyField(
        to='personnel.User',
        db_constraint=False,
        related_name='Task_sub',
        blank=True,
        verbose_name='参与者'
    )

    project = models.SmallIntegerField(blank=True, null=True,
                                       verbose_name='关联-(project) 项目信息')

    def __str__(self):
        return self.title


# 任务单日志
class TaskLogs(BaseModel):

    title = models.CharField(max_length=64, verbose_name='操作信息')
    content = models.TextField(verbose_name='日志内容')
    user_name = models.CharField(max_length=64, verbose_name='操作人名字')

    task = models.SmallIntegerField(verbose_name='关联-(task) 任务单')


# 工作日志
class WorkLogs(BaseModel):

    work_status = models.SmallIntegerField(
        verbose_name='工作状态')
    issue_status = models.CharField(blank=True, null=True,
        max_length=64, verbose_name='问题状态')
    other_env = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(OtherEnv) 工作环境')
    special_env = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(SpecialEnv) 特殊环境')
    isDrive = models.BooleanField(blank=True, null=True,
                                  verbose_name='是否开车')
    car_rental = models.SmallIntegerField(blank=True, null=True,
                                          verbose_name='关联-(CarRental) 租车情况')
    cart_fee = models.SmallIntegerField(blank=True, null=True,
        verbose_name='租车费')
    other_fee = models.SmallIntegerField(blank=True, null=True,
        verbose_name='其它车费')
    plan = models.TextField(verbose_name='明日计划')
    content = models.TextField(blank=True, null=True,
                               verbose_name='正文')
    finish_time = models.DateTimeField(blank=True, null=True, verbose_name='预计完成时间')

    project = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(project) 项目')
    user = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(user) 汇报人')
    ln_worklog = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(WorkLog) 项目')
    submitted = models.BooleanField(default=False)


# 工作总结
class Summary(BaseModel):

    worklog = models.SmallIntegerField(blank=True, null=True,
        verbose_name='日志汇报')
    project = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(Project) 项目')
    facility =models.SmallIntegerField(
        blank=True, null=True,
        verbose_name='关联-(Facility) 项目设备')
    outsourcer = models.SmallIntegerField(
        blank=True, null=True,
        verbose_name='关联-(Outsourcer) 承包商')
    content = models.TextField(blank=True, null=True,
                               verbose_name='正文')
    user = models.SmallIntegerField(blank=True, null=True,
        verbose_name='关联-(user) 汇报人')


class TaskFile(models.Model):

    title = models.CharField(max_length=64, blank=True, null=True, verbose_name='文件名称')
    file = models.FileField(upload_to=upload_path_file, blank=True, null=True,
                              verbose_name='附件')
    task = models.SmallIntegerField(verbose_name='关联-(task) 任务单')


##########
# 标签模型
##########

# 工作状态
class WorkStatus(models.Model):

    title = models.CharField(max_length=64,  verbose_name='工作状态')
    sort = models.SmallIntegerField(blank=True, null=True, verbose_name='排序')

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
        verbose_name = '工作状态'
        verbose_name_plural = verbose_name


# 工作环境
class OtherEnv(models.Model):

    title = models.CharField(max_length=64, verbose_name='工作环境')
    sort = models.SmallIntegerField(blank=True, null=True, verbose_name='排序')

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
        verbose_name = '工作环境'
        verbose_name_plural = verbose_name


# 工作环境
class SpecialEnv(models.Model):

    title = models.CharField(max_length=64, verbose_name='特殊工作环境')
    sort = models.SmallIntegerField(blank=True, null=True, verbose_name='排序')

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
        verbose_name = '特殊工作环境'
        verbose_name_plural = verbose_name


# 租车情况
class CarRental(models.Model):
    title = models.CharField(max_length=64, verbose_name='租车方式')
    sort = models.SmallIntegerField(blank=True, null=True, verbose_name='排序')

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
        verbose_name = '租车方式'
        verbose_name_plural = verbose_name


# 问题状态
class Issue_status(models.Model):
    title = models.CharField(max_length=64, verbose_name='问题状态')
    sort = models.SmallIntegerField(blank=True, null=True, verbose_name='排序')

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
        verbose_name = '问题状态'
        verbose_name_plural = verbose_name


# 任务状态
class Task_Status(models.Model):
    title = models.CharField(max_length=64, verbose_name='任务状态')
    sort = models.SmallIntegerField(blank=True, null=True, verbose_name='排序')

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
        verbose_name = '任务状态'
        verbose_name_plural = verbose_name


# 来源
class Task_Priority(models.Model):
    title = models.CharField(max_length=64, verbose_name='来源')
    sort = models.SmallIntegerField(blank=True, null=True, verbose_name='排序')

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
        verbose_name = '来源'
        verbose_name_plural = verbose_name
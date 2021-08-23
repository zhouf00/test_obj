from django.db import models
from datetime import datetime
# 1、基表
class BaseModel(models.Model):

    is_delete = models.BooleanField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    # 作为基表的Model不能 数据库中形成对的表、设置abstract = True
    class Meta:
        abstract = True

# 2、图片保存路径
def upload_path_image(instance, filename):
    # print('/'.join([datetime.today().strftime("%Y%m%d"), 'img', filename]))
    return '/'.join([datetime.today().strftime("%Y%m%d"), 'img', filename])

# 3、图片保存路径
def upload_path_file(instance, filename):
    # print('/'.join([datetime.today().strftime("%Y%m%d"), 'img', filename]))
    return '/'.join([datetime.today().strftime("%Y%m%d"), 'file', filename])
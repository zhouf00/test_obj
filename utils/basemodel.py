from django.db import models
# 1、基表
class BaseModel(models.Model):

    is_delete = models.BooleanField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)

    # 作为基表的Model不能 数据库中形成对的表、设置abstract = True
    class Meta:
        abstract = True


def upload_path_image(instance, filename):

    return '/'.join([str(instance.name), 'img', filename])
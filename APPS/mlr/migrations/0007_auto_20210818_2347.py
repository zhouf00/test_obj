# Generated by Django 2.2.6 on 2021-08-18 23:47

from django.db import migrations, models
import utils.basemodel


class Migration(migrations.Migration):

    dependencies = [
        ('mlr', '0006_taskfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskfile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=utils.basemodel.upload_path_image, verbose_name='附件'),
        ),
    ]

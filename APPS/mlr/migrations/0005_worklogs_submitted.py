# Generated by Django 2.2.6 on 2021-08-14 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mlr', '0004_auto_20210810_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklogs',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
    ]
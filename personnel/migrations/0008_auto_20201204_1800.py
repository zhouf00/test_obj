# Generated by Django 2.2.6 on 2020-12-04 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0007_auto_20201204_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='departments',
        ),
        migrations.RemoveField(
            model_name='user',
            name='dept_leader',
        ),
    ]

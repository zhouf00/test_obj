# Generated by Django 2.2.6 on 2020-10-23 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auth',
            name='memo',
            field=models.TextField(blank=True, null=True, verbose_name='备注'),
        ),
    ]

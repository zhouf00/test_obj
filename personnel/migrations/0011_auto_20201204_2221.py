# Generated by Django 2.2.6 on 2020-12-04 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personnel', '0010_auto_20201204_2137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='department',
            new_name='departments',
        ),
    ]
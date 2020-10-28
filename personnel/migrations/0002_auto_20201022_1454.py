# Generated by Django 2.2.6 on 2020-10-22 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personnel', '0001_initial'),
        ('rbac', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
        ('engineering', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='menu',
            field=models.ManyToManyField(db_constraint=False, related_name='department', to='rbac.Menu'),
        ),
        migrations.AddField(
            model_name='structure',
            name='parentid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='personnel.Structure', to_field='deptid', verbose_name='父类构架'),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ManyToManyField(db_constraint=False, related_name='user', to='personnel.Structure'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='leader_dept',
            field=models.ManyToManyField(blank=True, db_constraint=False, related_name='leader', to='personnel.Structure'),
        ),
        migrations.AddField(
            model_name='user',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='builders', to='engineering.Project'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]

# Generated by Django 2.2.6 on 2021-03-13 19:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='markettrace',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='markettrace', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='markethistory',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='markethistory', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='market',
            name='coadjutant',
            field=models.ManyToManyField(blank=True, db_constraint=False, related_name='market_co', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='market',
            name='type',
            field=models.ManyToManyField(db_constraint=False, related_name='market', to='product.Product'),
        ),
        migrations.AddField(
            model_name='market',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='market', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='linkman',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linkman', to='crm.Market'),
        ),
    ]
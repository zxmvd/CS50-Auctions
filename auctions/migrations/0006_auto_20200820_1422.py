# Generated by Django 3.0.7 on 2020-08-20 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200820_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='time',
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid_price',
            field=models.CharField(max_length=10),
        ),
    ]

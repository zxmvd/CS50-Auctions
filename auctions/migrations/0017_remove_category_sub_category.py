# Generated by Django 3.0.7 on 2020-08-24 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20200824_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='sub_category',
        ),
    ]

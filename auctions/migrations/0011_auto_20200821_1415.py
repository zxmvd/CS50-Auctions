# Generated by Django 3.0.7 on 2020-08-21 04:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_watched_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='watched_by',
        ),
        migrations.AddField(
            model_name='listing',
            name='watched_by',
            field=models.ManyToManyField(blank=True, related_name='watching_user', to=settings.AUTH_USER_MODEL),
        ),
    ]

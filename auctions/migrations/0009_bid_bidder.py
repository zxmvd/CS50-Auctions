# Generated by Django 3.0.7 on 2020-08-20 22:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200820_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='asBidder', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

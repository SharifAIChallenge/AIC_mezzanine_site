# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0049_auto_20160318_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffteam',
            name='image',
            field=models.ImageField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=b'staff/teams/icons/', null=True, verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='staffmember',
            name='role',
            field=models.CharField(max_length=150, verbose_name='role', blank=True),
        ),
    ]

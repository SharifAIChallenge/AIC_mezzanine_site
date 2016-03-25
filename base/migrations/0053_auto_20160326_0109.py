# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0052_auto_20160325_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffmember',
            name='image',
            field=models.ImageField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=b'staff/images/', null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='staffteam',
            name='icon',
            field=models.ImageField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=b'staff/teams/icons/', null=True, verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='code',
            field=models.FileField(upload_to=base.models.team_code_directory_path, storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='compiled_code',
            field=models.FileField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=base.models.team_compiled_code_directory_path, null=True, verbose_name='compiled code', blank=True),
        ),
    ]

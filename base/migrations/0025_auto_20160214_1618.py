# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_auto_20160214_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submit',
            name='code',
            field=models.FileField(upload_to=b'submits/temp', storage=AIC_site.storage.SyncingStorage(b'storages.backends.hashpath.HashPathStorage', b'storages.backends.sftpstorage.SFTPStorage'), verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='compile_log_file',
            field=models.TextField(null=True, verbose_name='log file', blank=True),
        ),
        migrations.AlterField(
            model_name='submit',
            name='compiled_code',
            field=models.FileField(storage=AIC_site.storage.SyncingStorage(b'storages.backends.hashpath.HashPathStorage', b'storages.backends.sftpstorage.SFTPStorage'), upload_to=b'submits/compiled', null=True, verbose_name='compiled code', blank=True),
        ),
    ]

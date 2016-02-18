# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_auto_20160218_1227'),
    ]

    operations = [
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

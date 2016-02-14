# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20160214_0442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='config',
        ),
        migrations.AddField(
            model_name='dockercontainer',
            name='cores',
            field=models.CommaSeparatedIntegerField(default=[1024], max_length=512, verbose_name='cores'),
        ),
        migrations.AddField(
            model_name='dockercontainer',
            name='memory',
            field=models.PositiveIntegerField(default=104857600, verbose_name='memory'),
        ),
        migrations.AddField(
            model_name='dockercontainer',
            name='swap',
            field=models.PositiveIntegerField(default=0, verbose_name='swap'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='composer',
            field=models.FileField(storage=AIC_site.storage.SyncingStorage(b'storages.backends.hashpath.HashPathStorage', b'storages.backends.sftpstorage.SFTPStorage'), upload_to=b'docker/composers', null=True, verbose_name='docker composer', blank=True),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='build_log',
            field=models.TextField(default='', verbose_name='build log', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='dockerfile',
            field=models.FileField(upload_to=b'docker/dockerfiles', storage=AIC_site.storage.SyncingStorage(b'storages.backends.hashpath.HashPathStorage', b'storages.backends.sftpstorage.SFTPStorage'), verbose_name='dockerfile'),
        ),
        migrations.AlterField(
            model_name='serverconfiguration',
            name='compiled_code',
            field=models.FileField(upload_to=b'server/compiled_code', storage=AIC_site.storage.SyncingStorage(b'storages.backends.hashpath.HashPathStorage', b'storages.backends.sftpstorage.SFTPStorage'), verbose_name='compiled code'),
        ),
    ]

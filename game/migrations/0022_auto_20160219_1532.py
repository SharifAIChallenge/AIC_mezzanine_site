# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0021_auto_20160219_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockercontainer',
            name='dockerfile_src',
            field=models.FileField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=b'docker/dockerfiles', null=True, verbose_name='dockerfile source', blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='log_file',
            field=models.FileField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=b'games/logs/', null=True, verbose_name='game log file', blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='status', choices=[(0, 'waiting'), (1, 'queued'), (2, 'running'), (3, 'finished'), (4, 'failed')]),
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='config',
            field=models.FileField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=game.models.game_config_directory_path, null=True, verbose_name='configuration file', blank=True),
        ),
    ]

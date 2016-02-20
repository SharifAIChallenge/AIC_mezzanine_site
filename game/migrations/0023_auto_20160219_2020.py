# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0022_auto_20160219_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockercontainer',
            name='dockerfile_src',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=b'docker/dockerfiles', null=True, verbose_name='dockerfile source', blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_type',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='game type', choices=[(0, 'manual'), (1, 'friendly'), (2, 'qualifications'), (3, 'finals'), (4, 'seeding')]),
        ),
        migrations.AlterField(
            model_name='game',
            name='log_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=b'games/logs/', null=True, verbose_name='game log file', blank=True),
        ),
        migrations.AlterField(
            model_name='gameconfiguration',
            name='config',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=game.models.game_config_directory_path, null=True, verbose_name='configuration file', blank=True),
        ),
    ]

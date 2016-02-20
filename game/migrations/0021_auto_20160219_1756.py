# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_auto_20160219_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameconfiguration',
            name='config',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=game.models.game_config_directory_path, null=True, verbose_name='configuration file', blank=True),
        ),
    ]

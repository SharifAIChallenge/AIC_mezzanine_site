# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_auto_20160219_0211'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('config', models.FileField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=game.models.game_config_directory_path, null=True, verbose_name='configuration file', blank=True)),
                ('description', models.CharField(max_length=200, verbose_name='description')),
                ('description_fa', models.CharField(max_length=200, null=True, verbose_name='description')),
                ('description_en', models.CharField(max_length=200, null=True, verbose_name='description')),
                ('is_public', models.BooleanField(default=False, verbose_name='public')),
                ('competition', models.ForeignKey(verbose_name='competition', to='game.Competition')),
            ],
            options={
                'verbose_name': 'Game Configuration',
                'verbose_name_plural': 'Game Configurations',
            },
        ),
        migrations.RemoveField(
            model_name='game',
            name='competition',
        ),
        migrations.AddField(
            model_name='game',
            name='game_config',
            field=models.ForeignKey(verbose_name='game configuration', to='game.GameConfiguration', null=True),
            preserve_default=False,
        ),
    ]

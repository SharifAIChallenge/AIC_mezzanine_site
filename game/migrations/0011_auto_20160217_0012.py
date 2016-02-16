# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20160215_2054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='composer',
        ),
        migrations.AddField(
            model_name='competition',
            name='logger',
            field=models.ForeignKey(related_name='+', verbose_name='game logger', blank=True, to='game.DockerContainer', null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='log_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=b'games/logs/', null=True, verbose_name='game log file', blank=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='server',
            field=models.ForeignKey(related_name='+', verbose_name='server container', blank=True, to='game.DockerContainer', null=True),
        ),
        migrations.AlterField(
            model_name='gameteamsubmit',
            name='score',
            field=models.DecimalField(default=0, verbose_name='score', max_digits=25, decimal_places=10),
        ),
    ]

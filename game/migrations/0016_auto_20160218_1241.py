# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_auto_20160218_1231'),
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
            field=models.FileField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=b'games/logs/', null=True, verbose_name='game log file', blank=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='server',
            field=models.ForeignKey(related_name='+', verbose_name='server container', blank=True, to='game.DockerContainer', null=True),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='cores',
            field=models.CommaSeparatedIntegerField(default=1024, max_length=512, verbose_name='cores'),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='tag',
            field=models.CharField(unique=True, max_length=50, verbose_name='tag'),
        ),
        migrations.AlterField(
            model_name='gameteamsubmit',
            name='score',
            field=models.DecimalField(default=0, verbose_name='score', max_digits=25, decimal_places=10),
        ),
    ]

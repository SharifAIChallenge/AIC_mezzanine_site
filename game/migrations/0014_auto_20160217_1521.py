# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import AIC_site.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20160217_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='logger',
        ),
        migrations.RemoveField(
            model_name='game',
            name='log_file',
        ),
        migrations.AddField(
            model_name='competition',
            name='composer',
            field=models.FileField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=b'docker/composers', null=True, verbose_name='docker composer', blank=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='server',
            field=models.ForeignKey(verbose_name='server container', blank=True, to='game.DockerContainer', null=True),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='cores',
            field=models.CommaSeparatedIntegerField(default=[1024], max_length=512, verbose_name='cores'),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='dockerfile_src',
            field=models.FileField(storage=AIC_site.storage.SyncingHashStorage('storages.backends.sftpstorage.SFTPStorage'), upload_to=b'docker/dockerfiles', null=True, verbose_name='dockerfile source', blank=True),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='tag',
            field=models.CharField(max_length=50, verbose_name='tag'),
        ),
        migrations.AlterField(
            model_name='gameteamsubmit',
            name='score',
            field=models.IntegerField(default=0, verbose_name='score'),
        ),
    ]

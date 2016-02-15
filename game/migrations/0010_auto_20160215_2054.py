# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20160214_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serverconfiguration',
            name='execute_container',
        ),
        migrations.AlterField(
            model_name='competition',
            name='server',
            field=models.ForeignKey(verbose_name='server container', blank=True, to='game.DockerContainer', null=True),
        ),
        migrations.DeleteModel(
            name='ServerConfiguration',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='status', choices=[(0, 'waiting'), (1, 'queued'), (2, 'running'), (3, 'finished')]),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='dockerfile_src',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=b'docker/dockerfiles', null=True, verbose_name='dockerfile source', blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='log_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=b'games/logs/', null=True, verbose_name='game log file', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20160210_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='compile_log_file',
            field=models.FileField(upload_to=b'', null=True, verbose_name='log file', blank=True),
        ),
        migrations.AddField(
            model_name='submit',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='status', choices=[(0, 'waiting'), (1, 'compiling'), (2, 'compiled'), (3, 'failed')]),
        ),
    ]

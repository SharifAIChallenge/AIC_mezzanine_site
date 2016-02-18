# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_auto_20160217_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='compile_time_limit',
            field=models.PositiveIntegerField(default=60, verbose_name='compile time limit (s)', blank=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='execution_time_limit',
            field=models.PositiveIntegerField(default=600, verbose_name='execution time limit (s)', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0022_auto_20160219_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='error_log',
            field=models.TextField(null=True, verbose_name='error log', blank=True),
        ),
    ]

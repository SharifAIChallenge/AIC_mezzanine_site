# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0064_lastgetreportstime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastgetreportstime',
            name='time',
            field=models.CharField(default=0, max_length=20, verbose_name='salam'),
        ),
    ]

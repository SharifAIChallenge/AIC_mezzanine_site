# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20160130_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='registration_finish_date',
            field=models.DateTimeField(null=True, verbose_name='registration finish date'),
        ),
        migrations.AddField(
            model_name='competition',
            name='registration_start_date',
            field=models.DateTimeField(null=True, verbose_name='registration start date'),
        ),
    ]

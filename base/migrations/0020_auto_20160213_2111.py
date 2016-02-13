# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20160213_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamerequest',
            name='accept_time',
            field=models.DateTimeField(null=True, verbose_name='accept time', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_gamerequest_made_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamerequest',
            name='accept_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='accept time', blank=True),
        ),
    ]

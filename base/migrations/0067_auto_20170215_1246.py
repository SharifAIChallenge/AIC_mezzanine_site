# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0066_auto_20170215_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastgetreportstime',
            name='time',
            field=models.IntegerField(default=0, verbose_name='salam'),
        ),
    ]

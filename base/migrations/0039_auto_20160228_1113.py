# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0038_auto_20160227_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0031_auto_20160302_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='counted_in_group',
            field=models.BooleanField(default=False),
        ),
    ]

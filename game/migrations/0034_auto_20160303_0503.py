# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0033_auto_20160303_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='doubleeliminationgroup',
            name='started',
            field=models.BooleanField(default=False),
        ),
    ]

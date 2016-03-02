# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0030_auto_20160301_2128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['name'], 'verbose_name': 'group'},
        ),
        migrations.AddField(
            model_name='competition',
            name='my_games_active',
            field=models.BooleanField(default=False),
        ),
    ]

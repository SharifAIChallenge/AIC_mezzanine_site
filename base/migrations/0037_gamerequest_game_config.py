# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_auto_20160219_1717'),
        ('base', '0036_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamerequest',
            name='game_config',
            field=models.ForeignKey(default=1, verbose_name='game configuration', to='game.GameConfiguration'),
            preserve_default=False,
        ),
    ]

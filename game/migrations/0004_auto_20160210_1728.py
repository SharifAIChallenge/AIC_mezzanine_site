# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20160207_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='pre_games',
            field=models.ManyToManyField(to='game.Game', verbose_name='pre games', blank=True),
        ),
    ]

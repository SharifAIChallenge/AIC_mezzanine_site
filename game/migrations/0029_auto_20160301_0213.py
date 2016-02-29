# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0028_auto_20160301_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='group',
            field=models.ForeignKey(to='game.Group', null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_type',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='game type', choices=[(0, 'manual'), (1, 'friendly'), (2, 'qualifications'), (3, 'finals'), (4, 'seeding'), (5, 'supplementary'), (6, 'groups')]),
        ),
        migrations.AlterField(
            model_name='teamscore',
            name='game_type',
            field=models.PositiveSmallIntegerField(verbose_name='game types', choices=[(0, 'manual'), (1, 'friendly'), (2, 'qualifications'), (3, 'finals'), (4, 'seeding'), (5, 'supplementary'), (6, 'groups')]),
        ),
    ]

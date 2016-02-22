# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_auto_20160219_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_type',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='game type', choices=[(0, 'manual'), (1, 'friendly'), (2, 'qualifications'), (3, 'finals'), (4, 'seeding'), (5, 'supplementary')]),
        ),
    ]

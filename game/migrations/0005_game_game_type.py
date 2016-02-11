# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20160210_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_type',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='game type', choices=[(0, 'manual'), (1, 'friendly'), (2, 'qualifications'), (3, 'finals')]),
        ),
    ]

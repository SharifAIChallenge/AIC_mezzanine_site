# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0043_game_run_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='log',
            field=models.TextField(null=True, blank=True),
        ),
    ]

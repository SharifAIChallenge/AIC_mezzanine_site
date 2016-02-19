# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0019_auto_20160219_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_config',
            field=models.ForeignKey(verbose_name='game configuration', to='game.GameConfiguration', null=True),
        ),
    ]

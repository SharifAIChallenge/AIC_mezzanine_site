# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0034_auto_20160303_0503'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doubleeliminationgroup',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='doubleeliminationteamproxy',
            options={'ordering': ['id']},
        ),
    ]

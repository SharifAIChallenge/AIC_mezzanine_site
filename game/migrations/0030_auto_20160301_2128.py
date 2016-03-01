# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0029_auto_20160301_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='submit_active',
            field=models.BooleanField(default=False),
        ),
    ]

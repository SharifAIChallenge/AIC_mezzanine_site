# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0050_auto_20160318_1945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffteam',
            old_name='image',
            new_name='icon',
        ),
    ]

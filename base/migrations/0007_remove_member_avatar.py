# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_team_show'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='avatar',
        ),
    ]

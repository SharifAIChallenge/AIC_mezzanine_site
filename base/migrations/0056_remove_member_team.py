# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0055_auto_20170205_2215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='team',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20160202_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]

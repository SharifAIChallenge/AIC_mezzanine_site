# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_auto_20160301_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='id2',
            field=models.CharField(db_index=True, max_length=100, unique=True, null=True, blank=True),
        ),
    ]

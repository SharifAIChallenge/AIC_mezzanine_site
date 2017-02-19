# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0042_programminglanguage_code_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='run_id',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]

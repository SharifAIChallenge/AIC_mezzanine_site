# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='status', choices=[(0, 'waiting'), (1, 'queued'), (2, 'running'), (3, 'finished')]),
        ),
    ]

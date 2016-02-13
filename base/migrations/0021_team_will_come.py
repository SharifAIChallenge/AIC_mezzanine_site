# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_auto_20160213_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='will_come',
            field=models.PositiveSmallIntegerField(default=2, verbose_name='will come to site', choices=[(0, 'yes'), (1, 'no'), (2, 'not decided yet')]),
        ),
    ]

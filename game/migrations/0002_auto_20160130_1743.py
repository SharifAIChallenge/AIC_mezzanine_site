# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='max_members',
            field=models.PositiveSmallIntegerField(default=3, verbose_name='max team members count'),
        ),
        migrations.AddField(
            model_name='competition',
            name='min_members',
            field=models.PositiveSmallIntegerField(default=3, verbose_name='min team members count'),
        ),
    ]

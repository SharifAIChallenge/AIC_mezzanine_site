# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='teams',
            field=models.ManyToManyField(to='base.Team', verbose_name='teams', through='base.TeamMember', blank=True),
        ),
    ]

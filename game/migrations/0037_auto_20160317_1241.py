# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0046_auto_20160317_1218'),
        ('game', '0036_competition_staff_teams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='staff_teams',
        ),
        migrations.AddField(
            model_name='competition',
            name='staff_team',
            field=models.ForeignKey(verbose_name='staff', blank=True, to='base.StaffTeam', null=True),
        ),
    ]

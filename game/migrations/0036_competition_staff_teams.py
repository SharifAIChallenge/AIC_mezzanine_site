# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_staffmember_staffteam'),
        ('game', '0035_auto_20160303_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='staff_teams',
            field=models.ManyToManyField(to='base.StaffTeam', verbose_name='staff teams', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0046_auto_20160317_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffteam',
            name='parent',
            field=models.ForeignKey(related_name='sub_teams', verbose_name='parent team', blank=True, to='base.StaffTeam', null=True),
        ),
    ]

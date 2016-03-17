# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0045_staffmember_staffteam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffteam',
            name='members',
            field=models.ManyToManyField(related_name='teams', verbose_name='team members', to='base.StaffMember', blank=True),
        ),
    ]

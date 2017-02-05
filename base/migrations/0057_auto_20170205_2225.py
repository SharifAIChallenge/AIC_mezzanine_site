# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0056_remove_member_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='head',
        ),
        migrations.AlterField(
            model_name='teammember',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='is_head',
            field=models.BooleanField(default=False),
        ),
    ]

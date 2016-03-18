# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_auto_20160318_0148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staffmember',
            options={'ordering': ('name',), 'verbose_name': 'staff member', 'verbose_name_plural': 'staff'},
        ),
        migrations.AddField(
            model_name='staffteam',
            name='level',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffteam',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffteam',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffteam',
            name='tree_id',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staffteam',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='sub_teams', verbose_name='parent team', blank=True, to='base.StaffTeam', null=True),
        ),
    ]

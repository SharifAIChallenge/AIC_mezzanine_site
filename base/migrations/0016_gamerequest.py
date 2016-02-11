# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_game_game_type'),
        ('base', '0015_auto_20160210_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.NullBooleanField(verbose_name='state')),
                ('accept_time', models.DateTimeField(verbose_name='accept time')),
                ('game', models.ForeignKey(to='game.Game', null=True)),
                ('requestee', models.ForeignKey(related_name='+', verbose_name='requestee', to='base.Team')),
                ('requester', models.ForeignKey(related_name='+', verbose_name='requester', to='base.Team')),
            ],
        ),
    ]

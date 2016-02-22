# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0026_auto_20160222_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(verbose_name='score')),
                ('game_type', models.PositiveSmallIntegerField(verbose_name='game types', choices=[(0, 'manual'), (1, 'friendly'), (2, 'qualifications'), (3, 'finals'), (4, 'seeding'), (5, 'supplementary')])),
                ('team', models.ForeignKey(verbose_name='team', to='base.Team')),
            ],
            options={
                'verbose_name': 'score',
            },
        ),
        migrations.AlterUniqueTogether(
            name='teamscore',
            unique_together=set([('team', 'game_type')]),
        ),
    ]

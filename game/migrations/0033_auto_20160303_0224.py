# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0032_auto_20160302_0516'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoubleEliminationGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('finished', models.BooleanField(default=False)),
                ('games_csv', models.TextField(blank=True)),
                ('competition', models.ForeignKey(related_name='double_elimination_groups', verbose_name='competition', to='game.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='DoubleEliminationTeamProxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(default=0, verbose_name='score', max_digits=25, decimal_places=10)),
                ('source_rank', models.PositiveSmallIntegerField(default=0)),
                ('group', models.ForeignKey(related_name='teams', to='game.DoubleEliminationGroup')),
                ('source_group', models.ForeignKey(related_name='+', to='game.DoubleEliminationGroup', null=True)),
                ('team', models.ForeignKey(to='base.Team', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='counted_in_double_elimination_group',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='double_elimination_group',
            field=models.ForeignKey(to='game.DoubleEliminationGroup', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20160128_2013'),
        ('game', '0003_auto_20160128_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameTeamSubmit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0, verbose_name='score')),
            ],
            options={
                'ordering': ('score',),
            },
        ),
        migrations.RemoveField(
            model_name='gameteam',
            name='game',
        ),
        migrations.RemoveField(
            model_name='gameteam',
            name='team',
        ),
        migrations.AlterField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='base.Submit', verbose_name='players', through='game.GameTeamSubmit'),
        ),
        migrations.DeleteModel(
            name='GameTeam',
        ),
        migrations.AddField(
            model_name='gameteamsubmit',
            name='game',
            field=models.ForeignKey(verbose_name='game', to='game.Game'),
        ),
        migrations.AddField(
            model_name='gameteamsubmit',
            name='submit',
            field=models.ForeignKey(verbose_name='team submit', to='base.Submit'),
        ),
    ]

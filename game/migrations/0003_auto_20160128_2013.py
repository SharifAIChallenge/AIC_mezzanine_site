# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_competition_site'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'verbose_name': 'competition', 'verbose_name_plural': 'competitions'},
        ),
        migrations.AlterModelOptions(
            name='game',
            options={'verbose_name': 'game', 'verbose_name_plural': 'games'},
        ),
        migrations.AlterField(
            model_name='competition',
            name='site',
            field=models.OneToOneField(null=True, verbose_name='site', to='sites.Site'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='game',
            name='competition',
            field=models.ForeignKey(verbose_name='competition', to='game.Competition'),
        ),
        migrations.AlterField(
            model_name='game',
            name='config',
            field=models.FileField(upload_to=b'', verbose_name='config'),
        ),
        migrations.AlterField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='base.Team', verbose_name='players', through='game.GameTeam'),
        ),
        migrations.AlterField(
            model_name='game',
            name='pre_games',
            field=models.ManyToManyField(to='game.Game', verbose_name='pre games'),
        ),
        migrations.AlterField(
            model_name='game',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='gameteam',
            name='game',
            field=models.ForeignKey(verbose_name='game', to='game.Game'),
        ),
        migrations.AlterField(
            model_name='gameteam',
            name='score',
            field=models.IntegerField(verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='gameteam',
            name='team',
            field=models.ForeignKey(verbose_name='team', to='base.Team'),
        ),
    ]

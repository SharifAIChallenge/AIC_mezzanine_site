# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name='timestamp')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('site', models.OneToOneField(null=True, verbose_name='site', to='sites.Site')),
            ],
            options={
                'verbose_name': 'competition',
                'verbose_name_plural': 'competitions',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name='timestamp')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('config', models.FileField(upload_to=b'', verbose_name='config')),
                ('competition', models.ForeignKey(verbose_name='competition', to='game.Competition')),
            ],
            options={
                'verbose_name': 'game',
                'verbose_name_plural': 'games',
            },
        ),
        migrations.CreateModel(
            name='GameTeamSubmit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0, verbose_name='score')),
                ('game', models.ForeignKey(verbose_name='game', to='game.Game')),
                ('submit', models.ForeignKey(verbose_name='team submit', to='base.Submit')),
            ],
            options={
                'ordering': ('score',),
            },
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='base.Submit', verbose_name='players', through='game.GameTeamSubmit'),
        ),
        migrations.AddField(
            model_name='game',
            name='pre_games',
            field=models.ManyToManyField(to='game.Game', verbose_name='pre games'),
        ),
    ]

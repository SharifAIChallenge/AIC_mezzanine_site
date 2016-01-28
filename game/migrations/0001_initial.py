# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('config', models.FileField(upload_to=b'')),
                ('competition', models.ForeignKey(to='game.Competition')),
            ],
        ),
        migrations.CreateModel(
            name='GameTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('game', models.ForeignKey(to='game.Game')),
                ('team', models.ForeignKey(to='base.Team')),
            ],
            options={
                'ordering': ('score',),
            },
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='base.Team', through='game.GameTeam'),
        ),
        migrations.AddField(
            model_name='game',
            name='pre_games',
            field=models.ManyToManyField(to='game.Game'),
        ),
    ]

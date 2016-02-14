# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_game_game_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='DockerContainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=50, verbose_name='tag')),
                ('description', models.TextField(verbose_name='description')),
                ('dockerfile', models.FileField(upload_to=b'dockerfiles/', verbose_name='compile dockerfile')),
                ('version', models.PositiveSmallIntegerField(default=1, verbose_name='version')),
                ('build_log', models.FileField(upload_to=b'', null=True, verbose_name='build log', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammingLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'title')),
                ('compile_container', models.ForeignKey(related_name='+', verbose_name='compile container', to='game.DockerContainer', null=True, blank=True)),
                ('execute_container', models.ForeignKey(related_name='+', verbose_name='execute container', to='game.DockerContainer', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServerConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=50, verbose_name='tag')),
                ('compiled_code', models.FileField(upload_to=b'', verbose_name='compiled code')),
                ('execute_container', models.ForeignKey(related_name='+', verbose_name='execute container', to='game.DockerContainer')),
            ],
        ),
        migrations.AddField(
            model_name='competition',
            name='composer',
            field=models.FileField(upload_to=b'', null=True, verbose_name='docker composer', blank=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='players_per_game',
            field=models.PositiveIntegerField(default=2, verbose_name='number of players per game', blank=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='additional_containers',
            field=models.ManyToManyField(related_name='_competition_additional_containers_+', verbose_name='additional containers', to='game.DockerContainer', blank=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='server',
            field=models.ForeignKey(verbose_name='server container', blank=True, to='game.DockerContainer', null=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='supported_langs',
            field=models.ManyToManyField(to='game.ProgrammingLanguage', verbose_name='supported languages', blank=True),
        ),
    ]

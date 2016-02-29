# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0027_auto_20160222_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePlace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
            ],
            options={
                'verbose_name': 'place',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('competition', models.ForeignKey(related_name='groups', verbose_name='competition', to='game.Competition')),
            ],
            options={
                'verbose_name': 'group',
            },
        ),
        migrations.CreateModel(
            name='GroupTeamSubmit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(default=0, verbose_name='score', max_digits=25, decimal_places=10)),
                ('group', models.ForeignKey(to='game.Group')),
                ('submit', models.ForeignKey(to='base.Submit')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='time',
            field=models.DateTimeField(null=True, verbose_name='time'),
        ),
        migrations.AddField(
            model_name='group',
            name='submits',
            field=models.ManyToManyField(to='base.Submit', through='game.GroupTeamSubmit'),
        ),
        migrations.AddField(
            model_name='game',
            name='place',
            field=models.ForeignKey(verbose_name='place', to='game.GamePlace', null=True),
        ),
    ]

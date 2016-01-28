# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_team_competition'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submit',
            options={'verbose_name': 'submit', 'verbose_name_plural': 'submits'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'team', 'verbose_name_plural': 'teams'},
        ),
        migrations.AlterModelOptions(
            name='teaminvitation',
            options={'verbose_name': 'invitation', 'verbose_name_plural': 'invitations'},
        ),
        migrations.AlterField(
            model_name='submit',
            name='code',
            field=models.FileField(upload_to=b'submits/temp', verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='played',
            field=models.IntegerField(default=0, verbose_name='played'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='team',
            field=models.ForeignKey(verbose_name='team', to='base.Team'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='won',
            field=models.IntegerField(default=0, verbose_name='won'),
        ),
        migrations.AlterField(
            model_name='team',
            name='competition',
            field=models.ForeignKey(verbose_name='competition', to='game.Competition', null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='members', through='base.TeamMember'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='team',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='teaminvitation',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='accepted'),
        ),
        migrations.AlterField(
            model_name='teaminvitation',
            name='member',
            field=models.ForeignKey(verbose_name='member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teaminvitation',
            name='slug',
            field=models.CharField(max_length=100, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='teaminvitation',
            name='team',
            field=models.ForeignKey(verbose_name='team', to='base.Team'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='member',
            field=models.ForeignKey(verbose_name='member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='team',
            field=models.ForeignKey(verbose_name='team', to='base.Team'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='timestamp'),
        ),
    ]

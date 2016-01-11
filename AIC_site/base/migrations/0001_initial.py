# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('code', models.FileField(upload_to=b'submits/temp')),
                ('played', models.IntegerField()),
                ('won', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TeamInvitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('slug', models.CharField(max_length=100)),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(to='base.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(to='base.Team')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='base.TeamMember'),
        ),
        migrations.AddField(
            model_name='submit',
            name='team',
            field=models.ForeignKey(to='base.Team'),
        ),
    ]

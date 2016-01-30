# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
        ('base', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='competition',
            field=models.ForeignKey(verbose_name='competition', to='game.Competition', null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='head',
            field=models.ForeignKey(related_name='+', verbose_name='team head', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='submit',
            name='team',
            field=models.ForeignKey(verbose_name='team', to='base.Team'),
        ),
        migrations.AddField(
            model_name='member',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='member',
            name='team',
            field=models.ForeignKey(verbose_name='team', to='base.Team', null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_member_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.NullBooleanField(verbose_name='accepted')),
                ('member', models.ForeignKey(verbose_name='member', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(verbose_name='team', to='base.Team')),
            ],
            options={
                'verbose_name': 'join request',
                'verbose_name_plural': 'join requests',
            },
        ),
    ]

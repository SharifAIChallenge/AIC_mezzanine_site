# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0066_auto_20170306_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharifID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('member', models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

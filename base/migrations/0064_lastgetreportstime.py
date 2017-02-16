# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0063_submit_compiled_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastGetReportsTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField(default=0, verbose_name='salam')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

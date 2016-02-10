# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_auto_20160209_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english_text', models.TextField()),
                ('persian_text', models.TextField()),
                ('from_date', models.DateTimeField()),
                ('to_date', models.DateTimeField()),
            ],
        ),
    ]

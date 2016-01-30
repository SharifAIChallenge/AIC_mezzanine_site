# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_member_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='country',
            field=django_countries.fields.CountryField(default=b'IR', max_length=2),
        ),
    ]

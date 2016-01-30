# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20160130_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]

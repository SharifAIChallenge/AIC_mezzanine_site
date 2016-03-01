# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_auto_20160229_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='payment_value',
            field=models.PositiveIntegerField(default=0, verbose_name='Payment value (rials)'),
        ),
    ]

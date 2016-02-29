# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0040_auto_20160229_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='paid',
        ),
        migrations.AddField(
            model_name='team',
            name='payment_value',
            field=models.PositiveIntegerField(default=0, verbose_name='Payment value'),
        ),
        migrations.AddField(
            model_name='team',
            name='should_pay',
            field=models.BooleanField(default=False, verbose_name='Should pay?'),
        ),
    ]

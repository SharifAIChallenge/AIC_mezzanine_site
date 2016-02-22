# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0043_auto_20160301_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='mobile_number',
            field=models.CharField(max_length=11, verbose_name='mobile number', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='national_code',
            field=models.CharField(max_length=10, null=True, verbose_name='national code', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone_number',
            field=models.CharField(max_length=20, verbose_name='phone number', blank=True),
        ),
    ]

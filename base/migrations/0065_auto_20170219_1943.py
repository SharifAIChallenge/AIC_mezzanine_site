# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0064_lastgetreportstime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submit',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='timestamp'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20160217_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockercontainer',
            name='cores',
            field=models.CommaSeparatedIntegerField(default=1024, max_length=512, verbose_name='cores'),
        ),
        migrations.AlterField(
            model_name='dockercontainer',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
    ]

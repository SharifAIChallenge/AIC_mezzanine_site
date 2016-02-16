# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20160217_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockercontainer',
            name='tag',
            field=models.CharField(unique=True, max_length=50, verbose_name='tag'),
        ),
    ]

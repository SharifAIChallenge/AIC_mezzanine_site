# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_auto_20160214_0405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submit',
            name='pl',
        ),
        migrations.AlterField(
            model_name='submit',
            name='compiled_code',
            field=models.FileField(upload_to=b'submtis/compiled', null=True, verbose_name='compiled code', blank=True),
        ),
    ]

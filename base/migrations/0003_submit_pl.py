# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20160130_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='pl',
            field=models.CharField(max_length=3, null=True, verbose_name='programming language', choices=[(b'jav', b'java'), (b'cpp', b'c++'), (b'py2', b'python2'), (b'py3', b'python3')]),
        ),
    ]

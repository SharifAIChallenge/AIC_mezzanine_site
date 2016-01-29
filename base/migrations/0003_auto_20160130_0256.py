# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20160129_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=models.ImageField(upload_to=b'', verbose_name='avatar', blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='education_place',
            field=models.CharField(max_length=255, verbose_name='education place', blank=True),
        ),
    ]

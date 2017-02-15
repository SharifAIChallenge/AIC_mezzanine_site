# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0060_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='token',
            field=models.CharField(default='salam', max_length=40),
            preserve_default=False,
        ),
    ]

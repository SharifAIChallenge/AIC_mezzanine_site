# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='subject',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0061_submit_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='run_id',
            field=models.CharField(default='khar', max_length=40),
            preserve_default=False,
        ),
    ]

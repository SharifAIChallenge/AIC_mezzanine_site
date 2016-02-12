# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_submit_submitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamerequest',
            name='made_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

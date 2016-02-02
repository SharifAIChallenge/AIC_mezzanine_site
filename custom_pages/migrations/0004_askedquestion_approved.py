# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pages', '0003_auto_20160202_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='askedquestion',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_remove_transaction_our_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='error',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]

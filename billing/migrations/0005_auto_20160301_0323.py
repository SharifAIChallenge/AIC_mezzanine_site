# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_transaction_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='bank',
            field=models.CharField(max_length=20, choices=[(b'2', b'tejarat'), (b'1', b'mellat')]),
        ),
    ]

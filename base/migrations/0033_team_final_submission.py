# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_auto_20160219_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='final_submission',
            field=models.ForeignKey(related_name='team_final_submission', verbose_name='final submission', to='base.Submit', null=True),
        ),
    ]

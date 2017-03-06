# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0065_auto_20170219_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='final_submission',
            field=models.ForeignKey(related_name='team_final_submission', verbose_name='final submission', blank=True, to='base.Submit', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_email_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='final',
            field=models.BooleanField(default=False, verbose_name='team is final'),
        ),
        migrations.AlterField(
            model_name='team',
            name='show',
            field=models.BooleanField(default=True, verbose_name='show team in public list'),
        ),
    ]

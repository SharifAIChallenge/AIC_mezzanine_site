# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pages', '0004_askedquestion_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='askedquestion',
            name='approved',
            field=models.BooleanField(default=True, verbose_name='Approved'),
        ),
    ]

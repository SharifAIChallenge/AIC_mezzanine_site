# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20160214_0403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockercontainer',
            name='dockerfile',
            field=models.FileField(upload_to=b'dockerfiles/', verbose_name='dockerfile'),
        ),
    ]

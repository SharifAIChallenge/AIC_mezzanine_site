# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='site',
            field=models.OneToOneField(null=True, to='sites.Site'),
        ),
    ]

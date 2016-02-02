# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pages', '0005_auto_20160202_2349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='askedquestion',
            old_name='approved',
            new_name='is_approved',
        ),
    ]

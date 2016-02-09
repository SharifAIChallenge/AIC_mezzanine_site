# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_auto_20160208_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]

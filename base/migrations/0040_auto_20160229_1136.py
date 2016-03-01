# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0039_auto_20160228_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='mobile_number',
            field=models.CharField(max_length=11, verbose_name='mobile_number', blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='national_code',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='site_participation_possible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='submit',
            name='code',
            field=models.FileField(upload_to=base.models.team_code_directory_path, storage=django.core.files.storage.FileSystemStorage(), verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='submit',
            name='compiled_code',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=base.models.team_compiled_code_directory_path, null=True, verbose_name='compiled code', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20160214_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dockercontainer',
            name='dockerfile',
        ),
        migrations.AddField(
            model_name='dockercontainer',
            name='dockerfile_src',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=b'docker/dockerfiles', null=True, verbose_name='dockerfile source', blank=True),
        ),
        migrations.AlterField(
            model_name='competition',
            name='composer',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(), upload_to=b'docker/composers', null=True, verbose_name='docker composer', blank=True),
        ),
        migrations.AlterField(
            model_name='serverconfiguration',
            name='compiled_code',
            field=models.FileField(upload_to=b'server/compiled_code', storage=django.core.files.storage.FileSystemStorage(), verbose_name='compiled code'),
        ),
    ]

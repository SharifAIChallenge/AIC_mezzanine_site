# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20160214_0403'),
        ('base', '0021_team_will_come'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='compiled_code',
            field=models.FileField(upload_to=b'submits/compiled', null=True, verbose_name='compiled code', blank=True),
        ),
        migrations.AddField(
            model_name='submit',
            name='lang',
            field=models.ForeignKey(verbose_name='programming language', to='game.ProgrammingLanguage', null=True),
        ),
    ]

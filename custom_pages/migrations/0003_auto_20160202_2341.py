# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pages', '0002_auto_20160202_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='askedquestion',
            name='question',
            field=models.CharField(help_text='Ask New Question', max_length=1024, verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='askedquestion',
            name='question_en',
            field=models.CharField(help_text='Ask New Question', max_length=1024, null=True, verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='askedquestion',
            name='question_fa',
            field=models.CharField(help_text='Ask New Question', max_length=1024, null=True, verbose_name='Question'),
        ),
    ]

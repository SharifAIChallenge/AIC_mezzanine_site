# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('custom_pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='askedquestion',
            name='answer_en',
            field=models.CharField(max_length=4096, null=True, verbose_name='Answer', blank=True),
        ),
        migrations.AddField(
            model_name='askedquestion',
            name='answer_fa',
            field=models.CharField(max_length=4096, null=True, verbose_name='Answer', blank=True),
        ),
        migrations.AddField(
            model_name='askedquestion',
            name='question_en',
            field=models.CharField(max_length=1024, null=True, verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='askedquestion',
            name='question_fa',
            field=models.CharField(max_length=1024, null=True, verbose_name='Question'),
        ),
        migrations.AddField(
            model_name='qapage',
            name='content_en',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='qapage',
            name='content_fa',
            field=mezzanine.core.fields.RichTextField(null=True, verbose_name='Content'),
        ),
    ]

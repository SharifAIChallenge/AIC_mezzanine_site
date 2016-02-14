# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db.migrations.operations.special import RunPython


def set_programming_languages(apps, schema_editor):
    # create currently existing languages
    ProgrammingLanguage = apps.get_model('game', 'ProgrammingLanguage')
    langs = {
        'jav': ProgrammingLanguage.objects.get_or_create(name='Java 8'),
        'cpp': ProgrammingLanguage.objects.get_or_create(name='C++ 11'),
        'py3': ProgrammingLanguage.objects.get_or_create(name='Python 3'),
    }

    Submit = apps.get_model('base', 'Submit')
    for submit in Submit.objects.all():
        print(str(type(submit.pl)) + ": " + submit.pl)
        submit.lang = langs[submit.pl]
        submit.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20160214_0403'),
    ]

    operations = [
        RunPython(
            set_programming_languages
        )
    ]

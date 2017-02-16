# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def move_name_to_code_name(apps,schema_editor):
    ProgramingLanguage = apps.get_model("game","ProgrammingLanguage")
    db_alias = schema_editor.connection.alias
    for programming_language in ProgramingLanguage.objects.using(db_alias):
        programming_language.code_name=''.join(programming_language.name.split())
        programming_language.save()

class Migration(migrations.Migration):

    dependencies = [
        ('game', '0041_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='programminglanguage',
            name='code_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.RunPython(move_name_to_code_name,migrations.RunPython.noop)
    ]

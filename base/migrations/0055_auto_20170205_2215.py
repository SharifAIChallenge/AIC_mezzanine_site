# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def make_many_teams(apps, schema_editor):
    """
        Adds the Team object in Member.team to the
        many-to-many relationship in Member.teams
    """
    Member = apps.get_model('base', 'Member')
    TeamMember = apps.get_model('base', 'TeamMember')

    for member in Member.objects.all():
        if member.team:
            TeamMember.objects.create(member=member,
                                      team=member.team,
                                      confirmed=True,
                                      is_head=member.team.head_id == member.id)


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0054_auto_20170205_2212'),
    ]

    operations = [
        migrations.RunPython(make_many_teams),
    ]

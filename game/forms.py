# -*- coding:utf-8 -*-
import datetime

from base.models import Team
from django import forms
from django.utils.translation import ugettext_lazy as _
from game.models import Game, GameConfiguration, TeamScore, Group, Competition, GroupTeamSubmit, GamePlace


class ScheduleForm(forms.Form):
    type = forms.ChoiceField(label=_('game type'), choices=Game.GAME_TYPES)
    name = forms.CharField(label=_('name'))
    file = forms.FileField(label=_('file'), help_text=_('csv'))

    def save(self):
        game_type = self.cleaned_data['type']
        csv_file = self.cleaned_data['file']
        for line in csv_file.readlines():
            teams = line.strip().split(',')
            group = Group.objects.get(name=teams[0])
            game_conf = GameConfiguration.objects.get(id=teams[1])
            place = GamePlace.objects.get(id=teams[2])
            time = datetime.datetime(*teams[3:8])
            Game.create([Team.objects.get(id=team) for team in teams], game_type=game_type, game_conf=game_conf,
                        title=self.cleaned_data['name'], group=group, place=place, time=time)


class UploadScoresForm(forms.Form):
    type = forms.ChoiceField(label=_('game type'), choices=Game.GAME_TYPES)
    file = forms.FileField(label=_('file'), help_text=_('csv'))

    def save(self):
        game_type = self.cleaned_data['type']
        csv_file = self.cleaned_data['file']
        team_scores = []
        for line in csv_file.readlines():
            team_score = line.strip().split(',')
            team_scores.append(TeamScore(team_id=team_score[0], score=team_score[1], game_type=game_type))
        TeamScore.objects.bulk_create(team_scores)


class GroupingForm(forms.Form):
    competition = forms.ModelChoiceField(queryset=Competition.objects.all(), label=_('competition'))
    file = forms.FileField(label=_('file'), help_text=_('csv'))

    def save(self):
        competition = self.cleaned_data['competition']
        csv_file = self.cleaned_data['file']
        for line in csv_file.readlines():
            group_info = line.strip().split(',')
            group = Group.objects.create(name=group_info[0], competition=competition)
            for team_id in group_info[1:]:
                GroupTeamSubmit.objects.create(submit=Team.objects.get(id=team_id).final_submission, group=group)


class TeamScoresForm(forms.Form):
    type = forms.ChoiceField(label=_('game type'), choices=Game.GAME_TYPES)

    def clean_type(self):
        game_type = self.cleaned_data['type']
        if game_type != 1 and Game.objects.filter(game_type=game_type).exclude(status__gt=2).exists():
            raise forms.ValidationError(_('there are unfinished games'))
        return game_type

    def save(self):
        game_type = self.cleaned_data['type']
        csv_text = ""
        for game in Game.objects.filter(game_type=game_type):
            for submit in game.gameteamsubmit_set.all():
                csv_text += "%d,%f," % (submit.submit.team_id, submit.score)
            csv_text = csv_text[:-1] + '\n'
        return csv_text

# -*- coding:utf-8 -*-
import json

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from game.forms import ScheduleForm, TeamScoresForm, UploadScoresForm, GroupingForm, DoubleEliminationForm
from game.models import Competition, Group, Game, GroupTeamSubmit, DoubleEliminationTeamProxy, DoubleEliminationGroup


@user_passes_test(lambda u: u.is_superuser)
def schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        form = ScheduleForm()
    return render(request, 'accounts/account_form.html', {'form': form, 'title': 'begin games'})


@user_passes_test(lambda u: u.is_superuser)
def get_team_scores(request):
    if request.method == 'POST':
        form = TeamScoresForm(data=request.POST)
        if form.is_valid():
            csv_text = form.save()
            return HttpResponse(csv_text, content_type='text/csv')
    else:
        form = TeamScoresForm()
    return render(request, 'accounts/account_form.html', {'form': form, 'title': 'get scores'})


@user_passes_test(lambda u: u.is_superuser)
def upload_scores(request):
    if request.method == 'POST':
        form = UploadScoresForm(files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('upload_scores')
    else:
        form = UploadScoresForm()
    return render(request, 'accounts/account_form.html', {'form': form, 'title': 'upload scores'})


@user_passes_test(lambda u: u.is_superuser)
def grouping(request):
    if request.method == 'POST':
        form = GroupingForm(files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('grouping')
    else:
        form = GroupingForm()
    return render(request, 'accounts/account_form.html', {'form': form, 'title': 'grouping'})


@user_passes_test(lambda u: u.is_superuser)
def double_elimination(request):
    if request.method == 'POST':
        form = DoubleEliminationForm(files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('double_elimination')
    else:
        form = DoubleEliminationForm()
    return render(request, 'accounts/account_form.html', {'form': form, 'title': 'double elimination'})


def groups(request):
    competition = Competition.objects.get(site_id=request.site_id)
    return render(request, 'game/scoreboard.html', {
        'competition': competition
    })


def group_schedule(request, group_id):
    gt = get_object_or_404(Group, pk=group_id)
    games = Game.objects.filter(game_type=6, group_id=group_id)
    return render(request, 'game/group.html', {
        'gt': gt,
        'games': games,
    })


def get_scores_ajax(request):
    competition = Competition.objects.get(site_id=request.site_id)
    scores = GroupTeamSubmit.objects.filter(group__competition=competition).values_list('submit_id', 'score')
    return HttpResponse(json.dumps([{'id': score[0], 'score': float(score[1])} for score in scores]),
                        content_type="application/json")


def bracket(request):
    return render(request, 'game/bracket.html')


def get_final_brackets(request):
    teams = [
        [detp.team.name for detp in
         DoubleEliminationTeamProxy.objects.filter(group=group)
         ] for group in DoubleEliminationGroup.objects.all()[:16]
        ]
    group_list = list(DoubleEliminationGroup.objects.all().order_by('id'))
    results = [
        [
            [group.get_scores() for group in group_list[0:16]],
            # [group.get_scores() for group in group_list[24:32]],
            # [group.get_scores() for group in group_list[44:48]],
            # [group.get_scores() for group in group_list[54:56]],
            # [group.get_scores() for group in group_list[59]],
        ],
        [
            [group.get_scores() for group in group_list[16:24]],
            # [group.get_scores() for group in group_list[40:32:-1]],
            # [group.get_scores() for group in group_list[44:40:-1]],
            # [group_list[49].get_scores(), group_list[48].get_scores(), group_list[51].get_scores(),
            #  group_list[50].get_scores()],
            # [group_list[52].get_scores(), group_list[53].get_scores()],
            # [group_list[57].get_scores(), group_list[56].get_scores()],
            # [group_list[58].get_scores()],
            # [group_list[60].get_scores()],
        ],
        [
            # [group_list[61].get_scores()],
            # [group_list[62].get_scores()],
        ]
    ]

    brackets = {"teams": teams, 'results': results}
    return HttpResponse(json.dumps(brackets), content_type='application/json')


def double_elimination_games(request, group_id):
    games = Game.objects.filter(double_elimination_group_id=group_id)
    return render(request, 'game/de_group.html', {'games': games})

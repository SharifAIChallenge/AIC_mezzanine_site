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
    brackets = {
        "teams": [
            [detp.team.name for detp in
             DoubleEliminationTeamProxy.objects.filter(group=group, source_group__isnull=True).distinct()]
            for group in DoubleEliminationGroup.objects.filter(teams__source_group__isnull=True).distinct()
            ],
        'results': [
            [
                [
                    [],
                ]
            ],
            [],
            []
        ]
    }

    return HttpResponse(json.dumps(brackets), content_type='application/json')

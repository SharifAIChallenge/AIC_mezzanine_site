# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from game.forms import ScheduleForm, TeamScoresForm, UploadScoresForm
from game.models import Competition, Group


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


def groups(request):
    competition = Competition.objects.get(site_id=request.site_id)
    return render(request, 'game/scoreboard.html', {
        'competition': competition
    })


def group_schedule(request, group_id):
    gt = get_object_or_404(Group, pk=group_id)
    return render(request, 'game/group.html', {
        'gt': gt,
    })

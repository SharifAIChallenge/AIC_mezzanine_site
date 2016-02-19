# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'game.views',
    url("^schedule$", 'schedule', name="schedule"),
    url("^scores$", 'get_team_scores', name="get_scores"),
)

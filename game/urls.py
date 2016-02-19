# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'game.views',
    url("^schedule$", 'schedule', name="schedule"),
)

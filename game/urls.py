# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'game.views',
    url("^schedule$", 'schedule', name="schedule"),
    url("^scores/get$", 'get_team_scores', name="get_scores"),
    url("^scores/upload$", 'upload_scores', name="upload_scores"),

    url("^grouping$", 'grouping', name="grouping"),
    url("^double-elimination$", 'double_elimination', name="double_elimination"),

    url(r'^groups$', 'groups', name="groups"),
    url(r'^groups/(?P<group_id>\d+)$', 'group_schedule', name='group_schedule'),
    url(r'^get-scores$', 'get_scores_ajax'),
    url(r'^bracket$', 'bracket', name="bracket"),
    url(r'^get-brackets', 'get_final_brackets'),
)

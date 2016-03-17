# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    'base.views',
    url("^submit$", 'submit', name='submit_code'),
    url("^register$", 'register_team', name='register_team'),
    url("^invite$", 'invite_member', name='invite_member'),
    url("^get/submission/(?P<submit_id>\d+).zip$", 'get_submission', name='get_submission'),
    url("^accept/(?P<slug>\w+)$", 'accept_invite', name='accept_invitation'),
    url("^list$", 'teams', name='teams_list'),
    url("^my$", 'my_team', name='my_team'),
    url("^games$", 'my_games', name='my_games'),
    url("^change_name/(?P<id>[0-9]+)$", 'change_team_name', name='change_team_name'),
    url("^remove$", 'remove', name='remove'),
    url("^accept-decline$", 'accept_decline_request', name='accept_decline'),
    url("^join/(?P<team_id>[0-9]+)$", 'request_join', name="request_join"),
    url("^finalize$", 'finalize', name="finalize"),
    url("^gamerequest/handle", 'handle_game_request', name='handle_game_request'),
    url("^gamerequest", 'game_request', name='game_request'),
    url("^compile_log", 'compile_log', name='compile_log'),
    url("^final_submission", 'final_submission', name='set_final_submission'),
    url("^play/$", 'play_log', name='play_log'),
    url("^scoreboard$", 'scoreboard', name="scoreboard"),
    url("^billing/", include('billing.urls')),
    url("^staff/$", 'staff_list', name="staff_list"),
)

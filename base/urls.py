# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'base.views',
    url("^submit$", 'submit', name='submit_code'),
    url("^register$", 'register_team', name='register_team'),
    url("^choose$", 'choose_team', name='choose_team'),
    url("^invite$", 'invite_member', name='invite_member'),
    url("^accept/(?P<slug>\w+)$", 'accept_invite', name='accept_invitation'),
)

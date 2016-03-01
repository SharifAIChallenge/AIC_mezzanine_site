# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from game.tasks import run_game

syncing_storage = settings.BASE_AND_GAME_STORAGE


class Competition(models.Model):
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    title = models.CharField(verbose_name=_('title'), max_length=200)
    site = models.OneToOneField(Site, verbose_name=_('site'), null=True)
    max_members = models.PositiveSmallIntegerField(verbose_name=_("max team members count"), default=3)
    min_members = models.PositiveSmallIntegerField(verbose_name=_("min team members count"), default=3)

    registration_start_date = models.DateTimeField(verbose_name=_("registration start date"), null=True)
    registration_finish_date = models.DateTimeField(verbose_name=_("registration finish date"), null=True)

    players_per_game = models.PositiveIntegerField(verbose_name=_("number of players per game"), default=2, blank=True)
    supported_langs = models.ManyToManyField('game.ProgrammingLanguage', verbose_name=_("supported languages"),
                                             blank=True)
    server = models.ForeignKey('game.DockerContainer', verbose_name=_("server container"), null=True, blank=True,
                               related_name='+')
    logger = models.ForeignKey('game.DockerContainer', verbose_name=_("game logger"), null=True, blank=True,
                               related_name='+')
    additional_containers = models.ManyToManyField('game.DockerContainer', verbose_name=_("additional containers"),
                                                   related_name='+', blank=True)

    compile_time_limit = models.PositiveIntegerField(verbose_name=_('compile time limit (s)'), default=60, blank=True)
    execution_time_limit = models.PositiveIntegerField(verbose_name=_('execution time limit (s)'), default=10 * 60,
                                                       blank=True)

    submit_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('competition')
        verbose_name_plural = _('competitions')


def game_config_directory_path(instance, filename):
    return 'games/config/{0}/{1}'.format(instance.competition.id, filename)


class GameConfiguration(models.Model):
    competition = models.ForeignKey('game.Competition', verbose_name=_('competition'), null=False, blank=False)
    config = models.FileField(verbose_name=_('configuration file'), upload_to=game_config_directory_path,
                              storage=syncing_storage, null=True, blank=True)
    description = models.CharField(verbose_name=_('description'), max_length=200, null=False, blank=False)
    is_public = models.BooleanField(verbose_name=_('public'), default=False)

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _('Game Configuration')
        verbose_name_plural = _('Game Configurations')


class ProgrammingLanguage(models.Model):
    name = models.CharField(verbose_name=_('title'), max_length=200)
    compile_container = models.ForeignKey('game.DockerContainer', verbose_name=_('compile container'), related_name='+',
                                          null=True, blank=True)
    execute_container = models.ForeignKey('game.DockerContainer', verbose_name=_('execute container'), related_name='+',
                                          null=True, blank=True)

    def __unicode__(self):
        return self.name


class DockerContainer(models.Model):
    tag = models.CharField(verbose_name=_('tag'), max_length=50, unique=True)
    description = models.TextField(verbose_name=_('description'), blank=True)
    dockerfile_src = models.FileField(verbose_name=_('dockerfile source'), upload_to='docker/dockerfiles',
                                      storage=syncing_storage, null=True, blank=True)
    version = models.PositiveSmallIntegerField(verbose_name=_('version'), default=1)
    cores = models.CommaSeparatedIntegerField(verbose_name=_('cores'), default=1024, max_length=512)
    memory = models.PositiveIntegerField(verbose_name=_('memory'), default=100 * 1024 * 1024)
    swap = models.PositiveIntegerField(verbose_name=_('swap'), default=0)
    build_log = models.TextField(verbose_name=_('build log'), blank=True)

    def __unicode__(self):
        return '%s:%d' % (self.tag, self.version)


class Game(models.Model):
    GAME_TYPES = (
        (0, _('manual')),
        (1, _('friendly')),
        (2, _('qualifications')),
        (3, _('finals')),
        (4, _('seeding')),
        (5, _('supplementary')),
        (6, _('groups')),
    )

    STATUSES = (
        (0, _('waiting')),
        (1, _('queued')),
        (2, _('running')),
        (3, _('finished')),
        (4, _('failed')),
    )

    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    title = models.CharField(verbose_name=_('title'), max_length=200)
    players = models.ManyToManyField('base.Submit', verbose_name=_('players'), through='game.GameTeamSubmit')
    log_file = models.FileField(verbose_name=_('game log file'), upload_to='games/logs/', null=True, blank=True,
                                storage=syncing_storage)
    error_log = models.TextField(verbose_name=_('error log'), null=True, blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUSES, default=0)

    pre_games = models.ManyToManyField('game.Game', verbose_name=_('pre games'), blank=True)

    game_type = models.PositiveSmallIntegerField(verbose_name=_('game type'), choices=GAME_TYPES, default=0)
    game_config = models.ForeignKey('game.GameConfiguration', verbose_name=_('game configuration'), null=True)

    time = models.DateTimeField(verbose_name=_('time'), null=True)
    place = models.ForeignKey('game.GamePlace', null=True, verbose_name=_('place'))

    group = models.ForeignKey('game.Group', null=True)

    class Meta:
        verbose_name = _('game')
        verbose_name_plural = _('games')

    def __unicode__(self):
        return self.title

    @property
    def get_log_url(self):
        return reverse('play_log') + '?game=%d&log=%s' % (self.id, os.path.basename(self.log_file.name))

    def get_log_link(self):
        return '<a href="%s">view log</a>' % (self.get_log_url,)

    get_log_link.allow_tags = True
    get_log_link.short_description = "Log link"

    @classmethod
    def create(cls, participants, game_type=1, game_conf=None, title=None):
        if not title:
            title = _('friendly game')
        if not game_conf:
            game_conf = GameConfiguration.objects.first()
        game = Game.objects.create(
            title=title,
            game_type=game_type,
            game_config=game_conf,
        )
        for participant in participants:
            GameTeamSubmit.objects.create(game=game, submit=participant.final_submit)
        run_game.delay(game.id)

    def get_participants(self):
        return [submit.team for submit in self.players.all()]

    def get_scores(self):
        for team in self.get_participants():
            yield GameTeamSubmit.objects.get(game_id=self.id, submit__team_id=team.id).score


class GameTeamSubmit(models.Model):
    submit = models.ForeignKey('base.Submit', verbose_name=_('team submit'))
    game = models.ForeignKey('game.Game', verbose_name=_('game'))

    score = models.DecimalField(verbose_name=_('score'), default=0, max_digits=25, decimal_places=10)

    class Meta:
        ordering = ('score',)


class TeamScore(models.Model):
    team = models.ForeignKey('base.Team', verbose_name=_('team'))
    score = models.FloatField(verbose_name=_('score'))
    game_type = models.PositiveSmallIntegerField(verbose_name=_('game types'), choices=Game.GAME_TYPES)

    class Meta:
        verbose_name = _('score')
        unique_together = ('team', 'game_type')


class GroupTeamSubmit(models.Model):
    group = models.ForeignKey('game.Group')
    submit = models.ForeignKey('base.Submit')

    score = models.DecimalField(verbose_name=_('score'), default=0, max_digits=25, decimal_places=10)


class Group(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    competition = models.ForeignKey(Competition, related_name='groups', verbose_name=_('competition'))
    submits = models.ManyToManyField('base.Submit', through=GroupTeamSubmit)

    class Meta:
        verbose_name = _('group')

    def __unicode__(self):
        return u"group %s" % self.name


class GamePlace(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))

    class Meta:
        verbose_name = _('place')

    def __unicode__(self):
        return self.name

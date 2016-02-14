# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from game.tasks import run_game


class Competition(models.Model):
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    title = models.CharField(verbose_name=_('title'), max_length=200)
    site = models.OneToOneField(Site, verbose_name=_('site'), null=True)
    max_members = models.PositiveSmallIntegerField(verbose_name=_("max team members count"), default=3)
    min_members = models.PositiveSmallIntegerField(verbose_name=_("min team members count"), default=3)

    registration_start_date = models.DateTimeField(verbose_name=_("registration start date"), null=True)
    registration_finish_date = models.DateTimeField(verbose_name=_("registration finish date"), null=True)

    players_per_game = models.PositiveIntegerField(verbose_name=_("number of players per game"), default=2, blank=True)
    supported_langs = models.ManyToManyField('game.ProgrammingLanguage', verbose_name=_("supported languages"), blank=True)
    composer = models.FileField(verbose_name=_("docker composer"), null=True, blank=True)
    server = models.ForeignKey('game.DockerContainer', verbose_name=_("server container"), null=True, blank=True)
    additional_containers = models.ManyToManyField('game.DockerContainer', verbose_name=_("additional containers"), related_name='+', blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('competition')
        verbose_name_plural = _('competitions')


class ServerConfiguration(models.Model):
    tag = models.CharField(verbose_name=_('tag'), max_length=50)
    compiled_code = models.FileField(verbose_name=_('compiled code'))
    execute_container = models.ForeignKey('game.DockerContainer', verbose_name=_('execute container'), related_name='+')

    def __unicode__(self):
        return self.tag


class ProgrammingLanguage(models.Model):
    name = models.CharField(verbose_name=_('title'), max_length=200)
    compile_container = models.ForeignKey('game.DockerContainer', verbose_name=_('compile container'), related_name='+', null=True, blank=True)
    execute_container = models.ForeignKey('game.DockerContainer', verbose_name=_('execute container'), related_name='+', null=True, blank=True)

    def __unicode__(self):
        return self.name


class DockerContainer(models.Model):
    tag = models.CharField(verbose_name=_('tag'), max_length=50)
    description = models.TextField(verbose_name=_('description'))
    dockerfile = models.FileField(verbose_name=_('dockerfile'), upload_to='dockerfiles/')
    version = models.PositiveSmallIntegerField(verbose_name=_('version'), default=1)
    build_log = models.FileField(verbose_name=_('build log'), null=True, blank=True)

    def __unicode__(self):
        return '%s:%d' % (self.tag, self.version)


class Game(models.Model):
    GAME_TYPES = (
        (0, _('manual')),
        (1, _('friendly')),
        (2, _('qualifications')),
        (3, _('finals')),
    )

    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    competition = models.ForeignKey('game.Competition', verbose_name=_('competition'))
    title = models.CharField(verbose_name=_('title'), max_length=200)
    players = models.ManyToManyField('base.Submit', verbose_name=_('players'), through='game.GameTeamSubmit')
    config = models.FileField(verbose_name=_('config'))

    pre_games = models.ManyToManyField('game.Game', verbose_name=_('pre games'), blank=True)

    game_type = models.PositiveSmallIntegerField(verbose_name=_('game type'), choices=GAME_TYPES, default=0)

    class Meta:
        verbose_name = _('game')
        verbose_name_plural = _('games')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.config:
            self.config = ''  # TODO: where are they?
        super(Game, self).save(*args, **kwargs)

    def get_log_url(self):
        # TODO: write this
        return ''

    def get_participants(self):
        return [submit.team for submit in self.players]

    def run(self):
        run_game.delay(self.id)


class GameTeamSubmit(models.Model):
    submit = models.ForeignKey('base.Submit', verbose_name=_('team submit'))
    game = models.ForeignKey('game.Game', verbose_name=_('game'))

    score = models.IntegerField(verbose_name=_('score'), default=0)

    class Meta:
        ordering = ('score',)

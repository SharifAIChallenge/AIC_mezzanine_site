# -*- coding: utf-8 -*-
import base64
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import SET_NULL
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField


class Member(AbstractUser):
    phone_number = models.CharField(verbose_name=_("phone_number"), max_length=20, blank=True)
    education_place = models.CharField(verbose_name=_("education place"), max_length=255, blank=True)
    country = CountryField(verbose_name=_("country"), blank_label=_("choose your country"), default='IR')
    team = models.ForeignKey('base.Team', verbose_name=_("team"), null=True, blank=True, on_delete=SET_NULL)


class Team(models.Model):
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    competition = models.ForeignKey('game.Competition', verbose_name=_('competition'), null=True)
    name = models.CharField(verbose_name=_('name'), max_length=200)
    head = models.ForeignKey('base.Member', verbose_name=_("team head"), related_name='+')
    show = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Team%d(%s)' % (self.id, self.name)

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def get_members(self):
        return self.member_set.exclude(pk=self.head.pk).distinct()


class Submit(models.Model):
    PL_CHOICES = (
        ('jav', 'java'),
        ('cpp', 'c++'),
        ('py2', 'python2'),
        ('py3', 'python3'),
    )

    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    code = models.FileField(verbose_name=_('code'), upload_to='submits/temp')
    team = models.ForeignKey(Team, verbose_name=_('team'))

    pl = models.CharField(verbose_name=_("programming language"), choices=PL_CHOICES, null=True, max_length=3)

    played = models.IntegerField(verbose_name=_('played'), default=0)
    won = models.IntegerField(verbose_name=_('won'), default=0)

    def __unicode__(self):
        return 'Submit %s for team %d' % (self.code.name.split('/')[-1], self.team.id)

    class Meta:
        verbose_name = _('submit')
        verbose_name_plural = _('submits')

    def save(self, *args, **kwargs):
        super(Submit, self).save(*args, **kwargs)
        code = self.code
        if code:
            oldfile = self.code.name
            newfile = 'submits/%d/%d' % (self.team_id, self.id)

            self.code.storage.delete(newfile)
            self.code.storage.save(newfile, code)
            self.code.name = newfile
            self.code.close()
            self.code.storage.delete(oldfile)

        super(Submit, self).save(*args, **kwargs)


class TeamInvitation(models.Model):
    accepted = models.BooleanField(verbose_name=_('accepted'), default=False)
    team = models.ForeignKey('base.Team', verbose_name=_('team'))
    member = models.ForeignKey('base.Member', verbose_name=_('member'))
    slug = models.CharField(verbose_name=_('slug'), max_length=100)

    def __init__(self, *args, **kwargs):
        super(TeamInvitation, self).__init__(*args, **kwargs)
        if not self.slug:
            self.slug = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)[:-1] \
                .replace('+', 'O').replace('/', 'O')

    def __unicode__(self):
        return str(_('invitation of {} to join {} [{}]')).decode('utf-8') \
            .format(self.member, self.team, u'✓' if self.accepted else u'✗')

    class Meta:
        verbose_name = _('invitation')
        verbose_name_plural = _('invitations')

    def accept(self):
        self.member.team = self.team
        self.member.save()
        self.accepted = True
        self.save()

    @property
    def accept_link(self):
        return 'http://' + settings.SITE_URL[:-1] + reverse('accept_invitation', args=(self.slug,))


class JoinRequest(models.Model):
    accepted = models.NullBooleanField(verbose_name=_('accepted'))
    team = models.ForeignKey('base.Team', verbose_name=_('team'))
    member = models.ForeignKey('base.Member', verbose_name=_('member'))

    def __unicode__(self):
        return str(_('invitation of {} to join {} [{}]')).decode('utf-8') \
            .format(self.member, self.team, u'✓' if self.accepted else u'✗')

    class Meta:
        verbose_name = _('join request')
        verbose_name_plural = _('join requests')

    def accept(self):
        self.member.team = self.team
        self.member.save()
        self.accepted = True
        self.save()

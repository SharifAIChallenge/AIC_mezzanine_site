# -*- coding: utf-8 -*-
import base64
import re
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import SET_NULL
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from game.models import Game, GameTeamSubmit

syncing_storage = settings.BASE_AND_GAME_STORAGE


class Member(AbstractUser):
    phone_number = models.CharField(verbose_name=_("phone_number"), max_length=20, blank=True)
    education_place = models.CharField(verbose_name=_("education place"), max_length=255, blank=True)
    country = CountryField(verbose_name=_("country"), blank_label=_("choose your country"), default='IR')
    team = models.ForeignKey('base.Team', verbose_name=_("team"), null=True, blank=True, on_delete=SET_NULL)


class Team(models.Model):
    WILL_COME_CHOICES = (
        (0, _('yes')),
        (1, _('no')),
        (2, _('not decided yet')),
    )

    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    competition = models.ForeignKey('game.Competition', verbose_name=_('competition'), null=True)
    name = models.CharField(verbose_name=_('name'), max_length=200)
    head = models.ForeignKey('base.Member', verbose_name=_("team head"), related_name='+')
    show = models.BooleanField(default=True, verbose_name=_("show team in public list"))
    final = models.BooleanField(default=False, verbose_name=_("team is final"))

    final_submission = models.ForeignKey('base.Submit', verbose_name=_('final submission'),
                                         related_name="team_final_submission", null=True)

    will_come = models.PositiveSmallIntegerField(verbose_name=_("will come to site"), choices=WILL_COME_CHOICES,
                                                 default=2)

    def __unicode__(self):
        return 'Team%d(%s)' % (self.id, self.name)

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def get_members(self):
        return self.member_set.exclude(pk=self.head.pk).distinct()

    @property
    def final_submit(self):
        if not self.final_submission:
            self.final_submission = self.submit_set.filter(status=2).last()
            self.save()
        return self.final_submission


def team_code_directory_path(instance, filename):
    return 'submit/code/{0}/{1}'.format(instance.team.id, filename)


def team_compiled_code_directory_path(instance, filename):
    return 'submit/compile/{0}/{1}'.format(instance.team.id, filename)


class Submit(models.Model):
    STATUSES = (
        (0, _('waiting')),
        (1, _('queued')),
        (2, _('compiling')),
        (3, _('compiled')),
        (4, _('failed')),
    )

    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    code = models.FileField(verbose_name=_('code'), upload_to=team_code_directory_path, storage=syncing_storage)
    team = models.ForeignKey(Team, verbose_name=_('team'))
    submitter = models.ForeignKey(Member, default=None, null=True, blank=True)

    compiled_code = models.FileField(verbose_name=_('compiled code'), upload_to=team_compiled_code_directory_path,
                                     null=True, blank=True, storage=syncing_storage)
    compile_log_file = models.TextField(verbose_name=_('log file'), null=True, blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_('status'), choices=STATUSES, default=0)

    lang = models.ForeignKey('game.ProgrammingLanguage', verbose_name=_('programming language'), null=True)

    played = models.IntegerField(verbose_name=_('played'), default=0)
    won = models.IntegerField(verbose_name=_('won'), default=0)

    def __unicode__(self):
        return 'Submit %s for team %d' % (self.code.name.split('/')[-1], self.team.id)

    class Meta:
        verbose_name = _('submit')
        verbose_name_plural = _('submits')


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
        return reverse('accept_invitation', args=(self.slug,))


class JoinRequest(models.Model):
    accepted = models.NullBooleanField(verbose_name=_('accepted'))
    team = models.ForeignKey('base.Team', verbose_name=_('team'))
    member = models.ForeignKey('base.Member', verbose_name=_('member'))

    def __unicode__(self):
        return str(_('request of {} to join {} [{}]')).decode('utf-8') \
            .format(self.member, self.team, u'✓' if self.accepted else u'✗')

    class Meta:
        verbose_name = _('join request')
        verbose_name_plural = _('join requests')

    def accept(self):
        self.member.team = self.team
        self.member.save()
        self.accepted = True
        self.save()


class Email(models.Model):
    receivers = models.TextField()
    text = RichTextField()
    subject = models.CharField(max_length=255, blank=True)

    @staticmethod
    def post_save_callback(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')
        if created:
            text = instance.text
            subject = instance.subject
            temp = instance.receivers
            mails = re.findall(r'[\w.]+@[\w.]+', temp)
            for mail in mails:
                send_mail(subject, text, None, [mail], html_message=text)


post_save.connect(Email.post_save_callback, sender=Email)


class Message(models.Model):
    english_text = models.TextField()
    persian_text = models.TextField()
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()


class GameRequest(models.Model):
    requester = models.ForeignKey('Team', verbose_name=_('requester'), related_name='+')
    requestee = models.ForeignKey('Team', verbose_name=_('requestee'), related_name='+')
    made_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    accepted = models.NullBooleanField(_('state'))
    accept_time = models.DateTimeField(_('accept time'), null=True, blank=True)
    game_config = models.ForeignKey('game.GameConfiguration', verbose_name=_('game configuration'), null=False)

    game = models.ForeignKey('game.Game', null=True)

    def is_responded(self):
        return self.accept_time is not None

    @classmethod
    def create(cls, requester, requestee, game_config):
        wait = cls.check_last_time(requester)
        if wait:
            return wait

        cls.objects.create(requester=requester, requestee=requestee, game_config=game_config)

    @classmethod
    def check_last_time(cls, team):
        # last_time = cls.objects.filter(requester=team, accepted=True).aggregate(Max('accept_time'))['accept_time__max']
        # if last_time:
        #     now = timezone.now()
        #     one_hour_before = now - datetime.timedelta(hours=1)
        #     seconds = (last_time - one_hour_before).total_seconds()
        #     if seconds > 0:
        #         return int(seconds / 60)
        # return False
        return False

    def accept(self, accepted):
        wait = GameRequest.check_last_time(self.requester)
        if wait:
            return wait

        self.accepted = accepted
        self.accept_time = timezone.now()
        if accepted:
            Game.create([self.requestee, self.requester], game_conf=self.game_config)
        self.save()

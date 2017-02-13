# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import base64
import datetime
import re
import uuid
import coreapi

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models import Max
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from game.models import Game, Competition

syncing_storage = settings.BASE_AND_GAME_STORAGE


class Member(AbstractUser):
    phone_number = models.CharField(verbose_name=_("phone number"), max_length=20, blank=True)
    mobile_number = models.CharField(verbose_name=_("mobile number"), max_length=11, blank=True)
    education_place = models.CharField(verbose_name=_("education place"), max_length=255, blank=True)
    country = CountryField(verbose_name=_("country"), blank_label=_("choose your country"), default='IR')
    teams = models.ManyToManyField('base.Team', verbose_name=_("teams"), blank=True,
                                   through="TeamMember")
    national_code = models.CharField(max_length=10, null=True, verbose_name=_("national code"), blank=True)

    @property
    def team(self):
        team_member = TeamMember.objects.filter(member=self,
                                                team__competition=Competition.get_current_instance(),
                                                confirmed=True).first()
        return team_member.team if team_member else None


class Team(models.Model):
    WILL_COME_CHOICES = (
        (0, _('yes')),
        (1, _('no')),
        (2, _('not decided yet')),
    )

    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    competition = models.ForeignKey('game.Competition', verbose_name=_('competition'), null=True)
    name = models.CharField(verbose_name=_('name'), max_length=200)
    show = models.BooleanField(default=True, verbose_name=_("show team in public list"))
    final = models.BooleanField(default=False, verbose_name=_("team is final"))
    site_participation_possible = models.BooleanField(default=False)

    final_submission = models.ForeignKey('base.Submit', verbose_name=_('final submission'),
                                         related_name="team_final_submission", null=True)

    will_come = models.PositiveSmallIntegerField(verbose_name=_("will come to site"), choices=WILL_COME_CHOICES,
                                                 default=2)
    should_pay = models.BooleanField(verbose_name=_("Should pay?"), default=False)
    payment_value = models.PositiveIntegerField(verbose_name=_("Payment value (rials)"), default=0)

    def __init__(self, *args, **kwargs):
        super(Team, self).__init__(*args, **kwargs)
        members = []
        if self.id:
            members = self.get_members()
        for i in range(Competition.get_current_instance().max_members):
            m = None
            if len(members) > i:
                m = members[i]

            field_name = "member_{}".format(i + 1)
            setattr(self, field_name, m)

    def __unicode__(self):
        return "Team%d(%s)" % (self.id, self.name)

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    @property
    def has_paid(self):
        return self.transactions.filter(status='v').exists()

    def get_members(self):
        q = self.member_set.all()
        if self.head:
            q = q.exclude(pk=self.head.pk)
        return q.distinct()

    @property
    def final_submit(self):
        if not self.final_submission:
            self.final_submission = self.submit_set.filter(status=3).last()
            self.save()
        return self.final_submission

    @property
    def has_successful_submit(self):
        return Submit.objects.filter(team=self, status=3).exists()

    @property
    def paid_site_price(self):
        from billing.models import Transaction
        transaction = Transaction.objects.filter(status='v', user__in=self.member_set)
        return len(transaction) > 0

    @property
    def is_finalized(self):
        competition = Competition.get_current_instance()
        if self.member_set.count() >= competition.min_members:
            for team_member in self.teammember_set.all():
                if not team_member.confirmed:
                    return False
            return True
        return False

    @property
    def head(self):
        team_member = TeamMember.objects.filter(team=self, is_head=True).first()
        return team_member.member if team_member else None


class TeamMember(models.Model):
    member = models.ForeignKey(Member)
    team = models.ForeignKey(Team)
    confirmed = models.BooleanField(default=False)
    is_head = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            if TeamMember.objects.filter(member=self.member,
                                         confirmed=True,
                                         team__competition__id=self.team.competition.id):
                raise Exception(u"یک نفر در دو تیم نمی‌تواند عضو باشد!")
        super(TeamMember, self).save(force_insert, force_update, using, update_fields)


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
    token = models.CharField(max_length=40)
    run_id = models.CharField(max_length=40)


    def __unicode__(self):
        return 'Submit %s for team %d' % (self.code.name.split('/')[-1], self.team.id)

    class Meta:
        verbose_name = _('submit')
        verbose_name_plural = _('submits')

    @staticmethod
    def compilation_request(submit_pk,code,lang):
        credientals = {settings.BASE_MIDDLE_BRAIN_API_IP: 'Token ' + settings.BASE_MIDDLE_BRAIN_TOKEN}
        transports = [coreapi.transports.HTTPTransport(credentials=credientals)]
        client = coreapi.Client(transports=transports)
        schema = client.get(settings.BASE_MIDDLE_BRAIN_API_SCHEMA)
        ans=client.action(schema,['storage','new_file','update'],params={'file':coreapi.utils.File(name='file', content=code)})
        submit=Submit.objects.get(pk=submit_pk)
        submit.token=ans['token']
        ans=client.action(schema,['run','run','create'],params={'data':[{'operation':'compile','parameters':{'language':lang,'code_zip':ans['token']}}]})
        submit.run_id = ans[0]['run_id']
        submit.save()

    def request_compilation_async(self):
        Submit.compilation_request(submit_pk=self.pk,code=self.code,lang=self.lang.code_name)


class StaffTeam(MPTTModel):
    name = models.CharField(verbose_name=_('team name'), max_length=100)
    parent = TreeForeignKey('self', verbose_name=_('parent team'), null=True, blank=True, related_name='sub_teams')
    members = models.ManyToManyField('StaffMember', verbose_name=_('team members'), blank=True, related_name='teams')
    icon = models.ImageField(verbose_name=_('icon'), upload_to='staff/teams/icons/', storage=syncing_storage, null=True)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.parent) if self.parent else self.name

    class Meta:
        verbose_name = _('staff team')
        verbose_name_plural = _('staff teams')


class StaffMember(models.Model):
    name = models.CharField(verbose_name=_('full name'), max_length=150)
    email = models.EmailField(blank=True)
    entrance_year = models.PositiveIntegerField(verbose_name=_('entrance year'))
    role = models.CharField(verbose_name=_('role'), max_length=150, blank=True)
    bio = models.CharField(verbose_name=_('biography'), max_length=300, blank=True)
    image = models.ImageField(verbose_name=_('image'), upload_to='staff/images/', storage=syncing_storage, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('staff member')
        verbose_name_plural = _('staff')
        ordering = ('name',)


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
        if self.accepted:
            return
        with transaction.atomic():
            team_member = TeamMember.objects.get(member=self.member, team=self.team)
            team_member.confirmed = True
            team_member.date_confirmed = datetime.datetime.now()
            team_member.save()
            self.accepted = True
            self.save()
            TeamMember.objects.filter(member=self.member,
                                      team__competition=self.team.competition,
                                      confirmed=False).delete()
            TeamInvitation.objects.filter(member=self.member,
                                          team__competition=self.team.competition,
                                          accepted=False).delete()
            if self.team.is_finalized:
                self.team.final = True
                self.team.save()

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
        TeamMember.objects.create(member=self.member, team=self.team, confirmed=True)
        self.accepted = True
        self.save()
        # self.member.team = self.team
        # self.member.save()
        # self.accepted = True
        # self.save()


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
        last_time = cls.objects.filter(requester=team, accepted=True).aggregate(Max('accept_time'))['accept_time__max']
        if last_time:
            now = timezone.now()
            one_hour_before = now - datetime.timedelta(minutes=15)
            seconds = (last_time - one_hour_before).total_seconds()
            if seconds > 0:
                return int(seconds / 60)
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

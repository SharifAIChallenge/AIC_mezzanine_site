import base64
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Member(AbstractUser):
    phone_number = models.CharField(verbose_name=_("phone_number"), max_length=20, blank=True)
    education_place = models.CharField(verbose_name=_("education place"), max_length=255)
    avatar = models.ImageField(verbose_name=_("avatar"))


class Team(models.Model):
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    competition = models.ForeignKey('game.Competition', verbose_name=_('competition'), null=True)
    name = models.CharField(verbose_name=_('name'), max_length=200)
    members = models.ManyToManyField(Member, verbose_name=_('members'), through='base.TeamMember')

    def __unicode__(self):
        return 'Team%d(%s)' % (self.id, self.name)

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')


class TeamMember(models.Model):
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    team = models.ForeignKey('base.Team', verbose_name=_('team'))
    member = models.ForeignKey(Member, verbose_name=_('member'))


class Submit(models.Model):
    timestamp = models.DateTimeField(verbose_name=_('timestamp'), auto_now=True)
    code = models.FileField(verbose_name=_('code'), upload_to='submits/temp')
    team = models.ForeignKey(Team, verbose_name=_('team'))

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
    member = models.ForeignKey(Member, verbose_name=_('member'))
    slug = models.CharField(verbose_name=_('slug'), max_length=100)

    def __init__(self, *args, **kwargs):
        super(TeamInvitation, self).__init__(*args, **kwargs)
        self.slug = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)[:-1] \
            .replace('+', 'O').replace('/', 'O')

    class Meta:
        verbose_name = _('invitation')
        verbose_name_plural = _('invitations')

    def accept(self):
        TeamMember.objects.create(member=self.member, team=self.team)
        self.accepted = True
        self.save()

    @property
    def accept_link(self):
        return settings.SITE_URL[:-1] + reverse('accept_invitation', args=(self.slug,))

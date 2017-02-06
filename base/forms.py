# -*- coding: utf-8 -*-
from django import forms
from django.db import transaction
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django_countries.widgets import CountrySelectWidget
from mezzanine.accounts.forms import ProfileForm as mezzanine_profile_form
from mezzanine.utils.email import send_mail_template

from base.models import Submit, Team, Member, TeamInvitation, TeamMember
from game.models import Game, Competition


class ProfileForm(mezzanine_profile_form):
    terms = forms.BooleanField(required=True, label=_("Accept Terms"),
                               help_text=_("terms_of_service_text"))

    class Meta:
        model = Member
        fields = (
            "first_name", "last_name", "phone_number", "country", "education_place", "email", "username",
        )
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        self.fields['education_place'].required = False


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ('lang', 'code',)

    def __init__(self, competition, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        self.fields['lang'].queryset = competition.supported_langs.all()


class TeamForm(forms.ModelForm):
    MEMBER_FIELD_NAME = u"member_{}"

    class Meta:
        model = Team
        fields = ('name',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TeamForm, self).__init__(*args, **kwargs)
        team_members = TeamMember.objects.filter(team=self.instance) \
            .order_by('-is_head', '-confirmed') if self.instance else []
        self.members = set() if not self.instance else [team_member.member for team_member in team_members]
        self.competition = Competition.get_current_instance()

        can_edit = self.user == self.instance.head if self.instance else False
        self.can_edit = can_edit

        for i in range(self.competition.max_members):
            member_field = forms.CharField(label=_("member {}").format(i + 1),
                                           required=i < self.competition.min_members)
            member_field.widget.attrs['placeholder'] = _("email or username")

            if i == 0 and can_edit:
                member_field.widget.attrs['readonly'] = ''
                member_field.initial = self.user.username

            elif self.instance and i < len(self.members):
                member_field.initial = self.members[i].username
                if not can_edit or team_members[i].confirmed:
                    member_field.widget.attrs['readonly'] = ''

            self.fields[self.MEMBER_FIELD_NAME.format(i)] = member_field
        self.old_team_members = TeamMember.objects.filter(team=self.instance) if self.instance else []

    def clean(self):
        self.members = set()
        cleaned_data = super(TeamForm, self).clean()
        if not self.can_edit:
            raise forms.ValidationError(_(u"just team's head can edit team"))
        for i in range(self.competition.max_members):
            member_identification = cleaned_data.get(self.MEMBER_FIELD_NAME.format(i))
            if member_identification and isinstance(member_identification, list):
                member_identification = member_identification[0]
            if i == 0:
                if member_identification != self.user.username:
                    raise forms.ValidationError(_("brother you are hitting wrong!"))
                self.members.add(self.user)
            else:
                if member_identification:
                    try:
                        member = Member.objects.get(Q(username=member_identification)
                                                    | Q(email=member_identification))
                        self.members.add(member)
                    except Member.DoesNotExist:
                        self.errors[self.MEMBER_FIELD_NAME.format(i)] = [_("this user has not account")]
        if len(self.members) < self.competition.min_members:
            raise forms.ValidationError(_("at least {} members required for team")
                                        .format(self.competition.min_members))
        if self.old_team_members:
            team_members_diff = [team_member if team_member.member not in self.members else None
                                 for team_member in self.old_team_members]
            for team_member in team_members_diff:
                if team_member and team_member.confirmed:
                    raise forms.ValidationError(_("you can not remove an accepted member"))

    def save(self, host=None, commit=True):
        is_edit = True if self.instance else False
        instance = super(TeamForm, self).save(commit=False)
        with transaction.atomic():
            if is_edit:
                TeamMember.objects.filter(team=instance).delete()
                TeamInvitation.objects.filter(team=instance).exclude(member__in=self.members).delete()
            else:
                instance.competition = self.competition
                instance.save()
            team_members = [TeamMember(member=member,
                                       team=instance,
                                       is_head=member == self.user,
                                       confirmed=member == self.user)
                            for member in self.members]
            TeamMember.objects.bulk_create(team_members)
        for member in self.members:
            if member == self.user:
                continue
            invitation, new = TeamInvitation.objects.update_or_create(team=instance,
                                                                      member=member,
                                                                      defaults={'accepted': False})
            send_mail_template(_('AIChallenge team invitation'),
                               'mail/invitation_mail',
                               '',
                               self.user.email,
                               context={'team': instance.name,
                                        'abs_link': invitation.accept_link,
                                        'current_host': host})

        return instance


class TeamNameForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'id')


class WillComeForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('will_come',)
        widgets = {'will_come': forms.RadioSelect}


class GameTypeForm(forms.Form):
    game_type = forms.ChoiceField(choices=Game.GAME_TYPES, label=_('game type'), initial=2)

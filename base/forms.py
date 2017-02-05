# -*- coding: utf-8 -*-
from base.models import Submit, Team, TeamInvitation, Member
from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.widgets import CountrySelectWidget
from game.models import Game
from mezzanine.accounts.forms import ProfileForm as mezzanine_profile_form
from mezzanine.utils.email import send_mail_template


class ProfileForm(mezzanine_profile_form):
    terms = forms.BooleanField(required=True, label=_("Accept Terms"),
                               help_text=_("terms_of_service_text"))

    class Meta:
        model = Member
        fields = (
            "first_name", "last_name", "phone_number", "country", "education_place", "email",
            "username"
        )
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        # self.fields['phone_number'].initial = "+989123456789"
        self.fields['education_place'].required = False


# class SubmitForm(forms.ModelForm):
#     class Meta:
#         model = Submit
#         fields = ('lang', 'code',)
#
#     def __init__(self, competition, *args, **kwargs):
#         super(SubmitForm, self).__init__(*args, **kwargs)
#         self.fields['lang'].queryset = competition.supported_langs.all()


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)

    def save(self, commit=True, user=None, competition=None):
        instance = super(TeamForm, self).save(commit=False)
        instance.competition = competition
        instance.head = user
        instance.save()
        user.teams.add(instance)
        user.save()
        return instance


class NewTeamForm(forms.Form):
    name = forms.CharField(label=u"نام تیم", required=False)
    member1 = forms.CharField(label=u"عضو اول (سرگروه)", required=False)
    member2 = forms.CharField(label=u"عضو دوم", required=False)
    member3 = forms.CharField(label=u"عضو سوم", required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.competition = kwargs.pop('competition')

        super(NewTeamForm, self).__init__(*args, **kwargs)
        if self.user.team(self.competition):  # TODO
            members = self.user.team(self.competition).get_members()
            if members.exists():
                self.fields['member2'].initial = members[0]
                self.fields['member2'].widget.attrs.update({'disabled': 'disabled'})
                if members.count() > 1:
                    self.fields['member3'].initial = members[1]
                    self.fields['member3'].widget.attrs.update({'disabled': 'disabled'})

            invitations = TeamInvitation.objects.filter(team=self.user.team(self.competition), accepted=False)
            if invitations.exists():
                self.fields['member3'].initial = invitations[0].member.email
                if invitations.count() > 1:
                    self.fields['member3'].initial = invitations[1].member.email

            self.fields['name'].initial = self.user.team(self.competition).name
            if self.user.id != self.user.team(self.competition).head_id:
                self.fields['name'].widget.attrs.update({'disabled': 'disabled'})
                self.fields['member2'].widget.attrs.update({'disabled': 'disabled'})
                self.fields['member3'].widget.attrs.update({'disabled': 'disabled'})
            self.fields['member1'].initial = self.user.team(self.competition).head.get_full_name()
        else:
            self.fields['member1'].initial = self.user.get_full_name()
        self.fields['member1'].widget.attrs.update({'disabled': 'disabled'})

    def save(self, competition, host):
        if self.user.team(competition):
            if self.user.id == self.user.team(competition).head_id:
                team = self.user.team(competition)
                team.name = self.cleaned_data.pop('name')
                team.save()
                team = self.user.team
            else:
                return
        else:
            team = Team.objects.create(competition=competition, head=self.user, name=self.cleaned_data.pop('name'))
            self.user.team = team
            self.user.save()
        TeamInvitation.objects.filter(team=team).update(accepted=True)
        for email in self.cleaned_data.values():
            user = Member.objects.get(email=email)
            invitation, new = TeamInvitation.objects.update_or_create(team=team, user=user,
                                                                      defaults={'accepted': False})
            if new:
                send_mail_template(_('AIChallenge team invitation'), 'mail/invitation_mail', '',
                                   self.member.email, context={'team': team.name,
                                                               'abs_link': invitation.accept_link,
                                                               'current_host': host})


class TeamNameForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'id')


class InvitationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        if not Member.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_('user not found'))
        self.member = Member.objects.get(email=self.cleaned_data['email'])
        return self.cleaned_data['email']

    def save(self, team, host):
        invitation, is_new = TeamInvitation.objects.get_or_create(member=self.member, team=team)
        send_mail_template(_('AIChallenge team invitation'), 'mail/invitation_mail', '',
                           self.member.email, context={'team': team.name,
                                                       'abs_link': invitation.accept_link,
                                                       'current_host': host})

# class WillComeForm(forms.ModelForm):
#     #
#     # def __init__(self, *args, **kwargs):
#     #     super(WillComeForm, self).__init__(*args, **kwargs)
#     #     self.fields['will_come'].label = _('Will you participate in Tehran site competition?')
#     #     self.fields['will_come'].widget.attrs = {
#     #         'class': 'with-gap'
#     #     }
#
#     class Meta:
#         model = Team
#         fields = ('will_come',)
#         widgets = {'will_come': forms.RadioSelect}
#
#
# class GameTypeForm(forms.Form):
#     game_type = forms.ChoiceField(choices=Game.GAME_TYPES, label=_('game type'), initial=2)

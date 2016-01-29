# -*- coding: utf-8 -*-
from base.models import Submit, Team, TeamMember, TeamInvitation, Member
from django import forms
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from mezzanine.accounts.forms import ProfileForm as mezzanine_profile_form


class ProfileForm(mezzanine_profile_form):
    class Meta:
        model = Member
        fields = ("first_name", "last_name", "phone_number", "education_place", "avatar", "email", "username")

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        self.fields['phone_number'].initial = "+989123456789"
        self.fields['education_place'].required = False
        self.fields['avatar'].required = False


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ('code',)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)

    def save(self, commit=True, user=None, competition=None):
        instance = super(TeamForm, self).save(commit=False)
        instance.competition = competition
        instance.save()
        TeamMember.objects.create(team=instance, member=user)
        return instance


class ChooseTeamForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ChooseTeamForm, self).__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(members=user)


class InvitationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        if not User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_('user not found'))
        return self.cleaned_data['email']

    def save(self, team):
        user = User.objects.get(email=self.cleaned_data['email'])
        invitation, is_new = TeamInvitation.objects.get_or_create(member=user, team=team)
        message = get_template('mail/invitation_mail.html').render(
                Context({'team': team.name, 'link': invitation.accept_link}))
        user.email_user(_('AIChallenge team invitation'),
                        _('you have been invited to team %(name)s, follow the link to accept:\n%(link)s') % {
                            'name': team.name, 'link': invitation.accept_link}, html_message=message)
        return

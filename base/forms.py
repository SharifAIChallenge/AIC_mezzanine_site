# -*- coding: utf-8 -*-
from base.models import Submit, Team, TeamInvitation, Member
from django import forms
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django_countries.widgets import CountrySelectWidget
from mezzanine.utils.email import send_mail_template
from mezzanine.accounts.forms import ProfileForm as mezzanine_profile_form


class ProfileForm(mezzanine_profile_form):
    class Meta:
        model = Member
        fields = (
            "first_name", "last_name", "phone_number", "country", "education_place", "avatar", "email", "username"
        )
        widgets = {'country': CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        # self.fields['phone_number'].initial = "+989123456789"
        self.fields['education_place'].required = False
        self.fields['avatar'].required = False


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Submit
        fields = ('pl', 'code',)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)

    def save(self, commit=True, user=None, competition=None):
        instance = super(TeamForm, self).save(commit=False)
        instance.competition = competition
        instance.head = user
        instance.save()
        user.team = instance
        user.save()
        return instance


class InvitationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        if not Member.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(_('user not found'))
        self.member = Member.objects.get(email=self.cleaned_data['email'])
        return self.cleaned_data['email']

    def save(self, team):
        invitation, is_new = TeamInvitation.objects.get_or_create(member=self.member, team=team)
        send_mail_template(_('AIChallenge team invitation'), 'mail/invitation_mail', '',
                           self.member.email, context={'team': team.name, 'link': 'http://%s' % invitation.accept_link})

        return

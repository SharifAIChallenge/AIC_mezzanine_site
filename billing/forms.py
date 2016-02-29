from base.models import Member
from django import forms


class UserCompletionForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('phone_number', 'mobile_number', 'national_code')
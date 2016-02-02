from django import forms
from .models import AskedQuestion


class AskedQuestionForm(forms.ModelForm):
    class Meta:
        model = AskedQuestion
        fields = ('question',)
        widgets = {
            'question': forms.Textarea(attrs={'class': "materialize-textarea"}),
        }

    def save(self, page, user, commit=True):
        instance = super(AskedQuestionForm, self).save(commit=False)
        instance.page = page
        instance.questioner = user
        if commit:
            instance.save()
        return instance


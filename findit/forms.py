from django import forms
from .models import Feedback


class feedBackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('email', 'content')
        labels = {'content': 'body'}
        widgets = {'content': forms.Textarea(attrs={'cols': 10, 'rows': 3})}

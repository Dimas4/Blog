from django import forms
from .models import Messages


class SendForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = [
            'content',
        ]

from django import forms
from .models import Posts


class FormCreateEdit(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            "title",
            "content",
            "image",
            "category"
        ]



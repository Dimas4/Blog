from django import forms
from .models import Posts
from accounts.models import UserProfile


def is_ethic(title):
    bad_world = ['!!!']
    for i in bad_world:
        if i in title:
            return True
    return False


class FormCreateEdit(forms.ModelForm):
    class Meta:
        model = Posts
        fields = [
            "title",
            "content",
            "image",
            "category"
        ]

    def clean(self, *args, **kwargs):
        image = self.cleaned_data['image']
        if not image:
            raise forms.ValidationError('Add image to this post!')
        
        title = self.cleaned_data['title']
        if is_ethic(title):
            raise forms.ValidationError('Bad worlds in title!')

        return super(FormCreateEdit, self).clean(*args, **kwargs)


class FormTest(forms.ModelForm):
    content = forms.CharField(max_length=100)


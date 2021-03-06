from django import forms


from baskets.models import Basket
from .models import Posts


def is_ethic(title):
    bad_world = ['']
    for i in bad_world:
        if i in title:
            return True
    return False


class FormBasket(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Some text...'}))

    class Meta:
        model = Basket
        fields = [
            'description'
        ]


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
        # if is_ethic(title):
        #     raise forms.ValidationError('Bad words in the title!')

        return super(FormCreateEdit, self).clean(*args, **kwargs)

from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django import forms


from .models import UserProfile


User = get_user_model()


class UploadImage(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'image'
        ]


class ChangePassword(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = [
            'password',
        ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password don't math!")
        if len(password) < 8:
            raise forms.ValidationError("Password less then 8 letters")
        return super(ChangePassword, self).clean(*args, **kwargs)


class ChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = User.objects.filter(username=username).exists()
            if not user:
                raise forms.ValidationError("This user does not exist")
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(LoginForm, self).clean(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2'
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        user_username = User.objects.filter(username=username)
        if user_username.exists():
            raise forms.ValidationError("A user with that username already exists.")
        if password != password2:
            raise forms.ValidationError("Password don't match")
        if len(password) < 8:
            raise forms.ValidationError("Password must me bigger then 8 characters")
        if password in [email, username]:
            raise forms.ValidationError("Password equal to email or username")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already exist")
        return super(RegisterForm, self).clean(*args, **kwargs)

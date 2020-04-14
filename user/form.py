from django import forms

from .models import Users

USER_TYPE = (
    (1, 'User'),
    (2, 'Admin'),
)

GENDER = (
    (1, 'Male'),
    (2, 'Female'),
)


class SignupForm(forms.ModelForm):
    username = forms.CharField( help_text='Required. Add a valid email address.')
    password1 = forms.CharField( widget=forms.PasswordInput, help_text='Required. Add a valid Password.')
    password2 = forms.CharField( widget=forms.PasswordInput, help_text='Required. Add a valid Password same as above.')

    class Meta:
        model = Users
        fields = ('username', 'password1', 'password2', 'name', 'user_type',)


class LoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('username', 'password1',)


class UploadForm(forms.Form):
    file = forms.FileField(help_text="Upload a CSV file")


from django import forms
from django.contrib.auth.models import User
from .models import Profile
from carpatianknights.news.models import ActiveRoute
from datetime import date


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.RegexField(regex=r'\d{9}')
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1970, date.today().year)))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Your email')
    password = forms.CharField(widget=forms.PasswordInput)


class TourRegistration(forms.Form):
    active_tours = forms.ModelChoiceField(
        queryset=ActiveRoute.objects.filter(status=True))

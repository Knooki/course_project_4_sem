from django.shortcuts import render
from django import forms
from .models import CustomUser
from django_countries.fields import CountryField
from django_countries import countries


class UserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    country = CountryField(choices=list(countries))
    password = forms.CharField()
    class Meta:
        model = CustomUser
        fields = "__all__"



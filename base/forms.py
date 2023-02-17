from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from base import models


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'name', 'username', 'email',
            'password1', 'password2'
        ]


class RoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'avatar', 'bio']
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from base import models


class UserLoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget \
            .attrs['placeholder'] = 'e.g. kttel@example.com'
        self.fields['password'].widget \
            .attrs['placeholder'] = '•••••••'


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
        exclude = ['host', 'topic', 'participants']


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'avatar', 'bio']

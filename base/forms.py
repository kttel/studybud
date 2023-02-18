from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)


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

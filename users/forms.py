from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": True,
                                                             'placeholder': 'Имя пользователя или Email'})
                               , max_length=25, min_length=3, label='Имя или email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

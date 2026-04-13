from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Registration form for new users.
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    """
    Login form for existing users.
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'})
    )


class FizzBuzzForm(forms.Form):
    """
    Form for FizzBuzz game input.
    """
    answer = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={'class': 'game-input', 'placeholder': 'Enter your answer', 'autofocus': True})
    )
    mode = forms.ChoiceField(
        required=False,
        choices=[
            ('cpu', 'User vs Computer'),
            ('pvp', 'User vs User'),
        ],
        widget=forms.HiddenInput(),
        initial='cpu'
    )


class TicTacToeForm(forms.Form):
    """
    Form for TicTacToe game move.
    """
    position = forms.IntegerField(
        required=True,
        min_value=0,
        max_value=8,
        widget=forms.HiddenInput()
    )
    mode = forms.ChoiceField(
        required=False,
        choices=[
            ('cpu', 'User vs Computer'),
            ('pvp', 'User vs User'),
        ],
        widget=forms.HiddenInput(),
        initial='cpu'
    )


class ChessMoveForm(forms.Form):
    """
    Form for Chess move input.
    """
    move = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.HiddenInput()
    )
    mode = forms.ChoiceField(
        required=False,
        choices=[
            ('cpu', 'User vs Computer'),
            ('pvp', 'User vs User'),
        ],
        widget=forms.HiddenInput(),
        initial='cpu'
    )

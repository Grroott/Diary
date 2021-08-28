from .models import Daily, Feedback
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from . validators import username_validation
from django.core.validators import MaxLengthValidator, MinLengthValidator


# Customized forms
class SelectDate(forms.DateInput):
    input_type = 'date'


class MyLoginAuthForm(AuthenticationForm):
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'id': 'view-pwd'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct Username & Password"
        ),
        'inactive': _("This account is inactive. Activation link is sent to your email."),
    }


# Forms
class NewContentForm(forms.ModelForm):
    class Meta:
        widgets = {'date': SelectDate(), 'width': '50'}
        model = Daily
        fields = ['date', 'content', 'bookmark']


class ContentEditForm(forms.ModelForm):
    class Meta:
        widgets = {'date': SelectDate()}
        model = Daily
        fields = ['date', 'content', 'bookmark']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        validators=[username_validation, MinLengthValidator(5), MaxLengthValidator(15)],
        help_text='Username should be Alphanumeric of length 5 to 15'
    )
    email = forms.EmailField()
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'view-pwd'}),

    )
    password2 = forms.CharField(
        label=_("Re-enter password"),
        widget=forms.PasswordInput(attrs={'id': 'view-pwd1'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'your_feedback']


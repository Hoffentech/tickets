from django import forms
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth import forms as django_forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.password_validation import validate_password

from core.models import User

class PasswordResetForm(PasswordResetForm):

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             label=_("Email"), max_length=75)

class PasswordResetConfirmForm(SetPasswordForm):

    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class LoginForm(django_forms.AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
                                label=_("Email"), max_length=75)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'js-toggle-password form-control form-control-lg'}), label=_("Password"),
        validators=[validate_password]
    )

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(request=request, *args, **kwargs)
        if request:
            email = request.GET.get("email")
            if email:
                self.fields["username"].initial = email

class SignupForm(forms.ModelForm):

    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_("Nombre"),
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label=_("Email"),
        error_messages={
            "unique": _(
                "This email has already been registered."
            )
        },
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=_("Contraseña"),
        validators=[validate_password]
    )

    next = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={ 'style': 'visibility: hidden'}),
            label=_("Next"),
    )    

    class Meta:
        model = User
        fields = ('email', 'name', 'next')
        required = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

    def save(self, request=None, commit=True):
        user = super(SignupForm, self).save(commit=False)
        name = self.cleaned_data["name"]
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']
        
class ChangePasswordForm(forms.ModelForm):

    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label=_("Email"), max_length=75)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=_("Password"),
        validators=[validate_password]
    )
    
    class Meta:
        model = User
        fields = ['email']

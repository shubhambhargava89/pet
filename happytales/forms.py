from django import forms
from django.conf import UserSettingsHolder
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms import fields, widgets
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

from happytales.models import Customer, Feedback, Report


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
                   'password2': forms.PasswordInput(attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("old Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=("Email"), max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))


class MyPasswordConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'mobile', 'locality', 'city', 'state', 'zipcode']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
                   'locality': forms.TextInput(attrs={'class': 'form-control'}),
                   'city': forms.TextInput(attrs={'class': 'form-control'}),
                   'state': forms.Select(attrs={'class': 'form-control'}),
                   'zipcode': forms.NumberInput(attrs={'class': 'form-control'})}


class feedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'mobile', 'city', 'state', 'pincode', 'description']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
                   'city': forms.TextInput(attrs={'class': 'form-control'}),
                   'state': forms.Select(attrs={'class': 'form-control'}),
                   'pincode': forms.NumberInput(attrs={'class': 'form-control'}),
                   'description': forms.TextInput(attrs={'class': 'form-control'})}

class reportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'mobile', 'city', 'state', 'pincode','pet_type','pet_breed',
                           'pet_location', 'description']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
                   'city': forms.TextInput(attrs={'class': 'form-control'}),
                   'state': forms.Select(attrs={'class': 'form-control'}),
                   'pincode': forms.NumberInput(attrs={'class': 'form-control'}),
                   'pet_type': forms.Select(attrs={'class': 'form-control'}),
                  'pet_breed': forms.TextInput(attrs={'class': 'form-control'}),
                  'pet_location': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.TextInput(attrs={'class': 'form-control'})}

# USER_CHOICES = [
#     ('D', 'Donor'),
#     ('P', 'Adopter'),
#     ('N', 'NGO'),
#     ('C', 'Customer')
# ]
# class SignupForm(forms.ModelForm):
#   user_type = forms.ChoiceField(choices=USER_CHOICES, required=True, widget=forms.RadioSelect)
#     class Meta:
#         model = Signup
#         fields = ["first_name", "last_name", "username", "email", "password1", "password2", "user_type"]
#         widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
#                    'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
#                    'city': forms.TextInput(attrs={'class': 'form-control'}),
#                    'state': forms.Select(attrs={'class': 'form-control'}),
#                    'pincode': forms.NumberInput(attrs={'class': 'form-control'}),
#                    'pet_type': forms.Select(attrs={'class': 'form-control'}),
#                   'pet_breed': forms.TextInput(attrs={'class': 'form-control'}),
#                   'pet_location': forms.TextInput(attrs={'class': 'form-control'}),
#                    'description': forms.TextInput(attrs={'class': 'form-control'})}
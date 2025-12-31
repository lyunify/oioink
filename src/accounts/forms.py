from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from PIL import Image

from .models import Account, Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=128, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email { account } is already in use.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) >= 5 and len(username) <= 30:
            try:
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(
                f'Username { username } is already in use.')
        else:
            raise forms.ValidationError(
                f'Username { username } must be between 5 and 30 characters.')


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid signin')


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(
                pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email { account } is already in use.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) >= 5 and len(username) <= 30:
            try:
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(
                f'Username { username } is already in use.')
        else:
            raise forms.ValidationError(
                f'Username { username } must be between 5 and 30 characters.')

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.email = self.cleaned_data['email'].lower()
        account.username = self.cleaned_data['username']
        if commit:
            account.save()
        return account


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'address', 'city', 'country']

    def clean_first_name(self):
        if self.is_valid():
            first_name = self.cleaned_data['first_name']
            return first_name

    def clean_last_name(self):
        if self.is_valid():
            last_name = self.cleaned_data['last_name']
            return last_name

    def clean_phone(self):
        if self.is_valid():
            phone = self.cleaned_data['phone']
            return phone

    def clean_address(self):
        if self.is_valid():
            address = self.cleaned_data['address']
            return address

    def clean_city(self):
        if self.is_valid():
            city = self.cleaned_data['city']
            return city

    def clean_country(self):
        if self.is_valid():
            country = self.cleaned_data['country']
            return country

    def save(self, commit=True, *args, **kwargs):
        profile = super().save(commit=False, *args, **kwargs)
        if commit:
            profile.save()
        return profile


class ProfileImageUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_image']

    def clean_profile_image(self):
        if self.is_valid():
            profile_image = self.cleaned_data['profile_image']
            return profile_image

    def save(self, commit=True, *args, **kwargs):
        profile = super().save(commit=False, *args, **kwargs)
        profile.profile_image = self.cleaned_data['profile_image']
        if commit:
            profile.save()
        return profile

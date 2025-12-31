from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .forms import SignUpForm, AccountAuthenticationForm, AccountUpdateForm, ProfileUpdateForm, ProfileImageUpdateForm
from .models import Account, Profile
from .tokens import account_activation_token
from .utils import send_activation_email


# Account Section =============================================================

@login_required
def account_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get('user_id')
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            context['success_message'] = 'Updated'
    else:
        form = AccountUpdateForm(instance=request.user)
    context['form'] = form
    return render(request, 'accounts/account.html', context)


def signin_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('myhome:home')
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('myhome:home')
    else:
        form = AccountAuthenticationForm()
    context['form'] = form
    return render(request, 'accounts/signin.html', context)


def signout_view(request):
    logout(request)
    return redirect('myhome:home')


def signup_view(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password1']
            user = authenticate(email=email, password=raw_password)
            user.profile.save()
            login(request, user)
            return redirect('myhome:home')
    else:
        form = SignUpForm()
    context['form'] = form
    return render(request, 'accounts/signup.html', context)


def signup_auth_view(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(request, user)
            return redirect('accounts:signup_verify')
    else:
        form = SignUpForm()
    context['form'] = form
    return render(request, 'accounts/signup.html', context)


def signup_verify_view(request):
    context = {}
    return render(request, 'accounts/signup_verify.html', context)


def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        user.profile.save()
        login(request, user)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('myhome:home')
    else:
        # return HttpResponse('Activation link is invalid!')
        return redirect('accounts:signup_invalid')


def must_authenticate_view(request):
    context = {}
    return render(request, 'accounts/must_authenticate.html', context)


def validate_username(request):
    # Check username availability
    username = request.GET.get('username', None)
    response = {
        'is_taken': Account.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


# Profile Section =============================================================

@login_required
def profile_view(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            context['success_message'] = 'Your profile has been updated!'
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'form': form
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_image_update_view(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        form = ProfileImageUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            context['success_message'] = 'Your profile image has been updated!'
            return redirect('accounts:profile')
    else:
        form = ProfileImageUpdateForm(instance=request.user.profile)
    context = {
        'form': form
    }
    return render(request, 'accounts/profile_image_update.html', context)


@login_required
def settings_view(request, *args, **kwargs):
    context = {}
    return render(request, 'accounts/settings.html', context)

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from hasker.profiles.forms import SignUpForm, SettingsForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save()
            with transaction.atomic():
                user_obj.avatar = form.cleaned_data.get('avatar')
                user_obj.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main_page')
    else:
        form = SignUpForm()
    return render(request, 'profiles/signup.html', {'form': form})


@login_required
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user_obj = form.save(commit=False)
            with transaction.atomic():
                if form.cleaned_data.get('avatar'):
                    user_obj.avatar = form.cleaned_data.get('avatar')
                user_obj.save()
            return redirect('main_page')

    else:
        form = SettingsForm(instance=request.user)
    return render(request, 'profiles/settings.html', {'form': form})

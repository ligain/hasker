from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from hasker.profiles.forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save()
            user_obj.profile.avatar = form.cleaned_data.get('avatar')
            user_obj.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main_page')
    else:
        form = SignUpForm()
    return render(request, 'profiles/signup.html', {'form': form})

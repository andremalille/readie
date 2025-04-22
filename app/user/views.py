from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserChangeInfoForm,
)


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('books')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('books')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def profile_view(request):
    user = request.user
    context = {'user': user}

    return render(request, 'profile.html', context)


def change_info_view(request):
    if request.method == 'POST':
        form = UserChangeInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('new_password'):
                user.set_password(form.cleaned_data['new_password'])
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserChangeInfoForm(instance=request.user)
    return render(request, 'change_profile.html', {'form': form})

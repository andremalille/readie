from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import (
    login,
    authenticate,
    logout,
    update_session_auth_hash
)
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserChangeInfoForm,
    UserNameForm,
)


def register_view(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('name')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_name_view(request):
    """Assign user name."""
    user = request.user
    if request.method == 'POST':
        form = UserNameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            user.name = name
            user.save()
            update_session_auth_hash(request, user)
            return redirect('books')
    else:
        form = UserNameForm()
    return render(request, 'user_name.html', {'form': form})


def login_view(request):
    """Login user to their account"""
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
    """Logs out user"""
    logout(request)
    return redirect('login')


@login_required()
def profile_view(request):
    """Display user's profile information"""
    user = request.user
    context = {'user': user}

    return render(request, 'profile.html', context)


@login_required()
def change_profile_image(request):
    """Change user's profile image"""
    if request.method == 'POST':
        if request.FILES.get('image'):
            request.user.image = request.FILES['image']
            request.user.save()
    return redirect('profile')


@login_required()
def change_info_view(request):
    """Change user's profile information."""
    if request.method == 'POST':
        form = UserChangeInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('new_password'):
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)
            else:
                user.save()
            return redirect('profile')
    else:
        form = UserChangeInfoForm(instance=request.user)
    return render(request, 'change_profile.html', {'form': form})

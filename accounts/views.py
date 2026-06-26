from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, ProfileEditForm, SignUpForm
from .models import UserProfile


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Welcome to Reddit, u/{user.username}!")
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "home")
            messages.success(request, f"Welcome back, u/{user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")


@login_required
def home_view(request):
    return render(request, "accounts/home.html")


def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_403(request, exception):
    return render(request, "errors/403.html", status=403)


def error_500(request):
    return render(request, "errors/500.html", status=500)


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)
    is_own = request.user == profile_user
    return render(
        request,
        "accounts/profile.html",
        {
            "profile_user": profile_user,
            "profile": profile,
            "is_own": is_own,
        },
    )


@login_required
def profile_edit_view(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, "accounts/profile_edit.html", {"form": form})

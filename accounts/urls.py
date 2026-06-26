from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="landing"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home_view, name="home"),
    path("u/<str:username>/", views.profile_view, name="profile"),
    path("settings/profile/", views.profile_edit_view, name="profile_edit"),
]

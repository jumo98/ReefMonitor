from django.urls import path
from django.contrib.auth import views as auth_views

from .views import login_view, register_user, logout_view, ResetPasswordView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_view, name="logout"),
    path("password_reset/", ResetPasswordView.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
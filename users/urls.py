from django.urls import path

from users.apps import UsersConfig
from users.views import (
    LoginView,
    LogoutView,
    RegisterView,
    VerificationFailedView,
    UserUpdateView,
    generate_new_password,
    VerifyEmailView,
    toggle_active,
    UserListView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile", UserUpdateView.as_view(), name="profile"),
    path("profile/genpassword/", generate_new_password, name="generate_new_password"),
    path("users/", UserListView.as_view(), name="users"),
    path("toggle_active/<int:pk>/", toggle_active, name="toggle_active"),
    path(
        "verify-email/<str:uidb64>/<str:token>/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path(
        "verification_failed/",
        VerificationFailedView.as_view(),
        name="verification_failed",
    ),
]

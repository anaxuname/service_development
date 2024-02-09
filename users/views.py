import random

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from users.forms import UserForm, UserRegisterForm
from users.models import User


# Create your views here.
class LoginView(BaseLoginView):
    template_name = "users/login.html"


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")
    template_name = "users/register.html"

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()
        token = default_token_generator.make_token(new_user)
        new_user.email_verification_token = token
        new_user.save()
        uid = urlsafe_base64_encode(force_str(new_user.pk).encode())
        verification_url = reverse("users:verify_email", kwargs={"uidb64": uid, "token": token})
        verification_url = self.request.build_absolute_uri(verification_url)
        send_mail(
            subject="Подтверждение электронной почты",
            message=render_to_string("users/verify_email.txt", {"verification_url": verification_url}),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


@login_required
def generate_new_password(request):
    new_password = "".join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject="Смена пароля",
        message=f"Ваш новый пароль:{new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False,
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse("main:index"))


@permission_required("users.set_user_deactivate")
def toggle_active(request, pk):
    """Пермиссия: функция для активации/деактивации пользователя"""
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse("users:users"))


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and user.email_verification_token == token:
            user.email_verified = True
            user.is_active = True
            user.save()
            return redirect("users:login")
        else:
            # Обработка ошибки подтверждения
            return redirect("users:verification_failed")


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy("users:profile")
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class VerificationFailedView(TemplateView):
    template_name = "users/verification_failed.html"


class UserListView(PermissionRequiredMixin, ListView):
    """Класс для просмотра списка пользователей"""

    permission_required = "users.view_all_users"
    model = User

    def get_queryset(self):
        return super().get_queryset().exclude(pk=self.request.user.pk).exclude(is_superuser=True)

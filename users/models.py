from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def is_content_manager(self):
        return self.groups.filter(name="Content Manager").exists()

    def is_moderator(self):
        return self.groups.filter(name="Moderator").exists()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("set_user_deactivate", "Can deactivate user"),
            ("view_all_users", "Can view all users"),
        ]

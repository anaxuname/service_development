from django.db import models

# Create your models here.
class Client(models.Model):

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=50, verbose_name='Firstname', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='Lastname', null=True, blank=True)
    comment = models.CharField(max_length=300, verbose_name='Comment', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.last_name
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

from django.conf import settings
from django.db import models


class StatusChoice(models.IntegerChoices):
    CREATED = 1, "Создана"
    PROCESSING = 2, "В обработке"
    COMPLETED = 3, "Завершена"
    ERROR = 4, "Ошибка"


class PeriodicityChoice(models.IntegerChoices):
    EVERY_DAY = 1, "Каждый день"
    EVERY_WEEK = 2, "Каждую неделю"
    EVERY_MONTH = 3, "Каждый месяц"


class NewsLetter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя рассылки')
    time_mailing = models.TimeField(verbose_name='Время отправки')
    periodicity_mailing = models.IntegerField(choices=PeriodicityChoice.choices, default=PeriodicityChoice.EVERY_DAY, verbose_name='Периодичность')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return f'{self.name} {self.time_mailing}'


class Message(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    body = models.TextField(verbose_name='Content')
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE)
    status_mailing = models.IntegerField(choices=StatusChoice.choices, default=StatusChoice.CREATED,
                                         verbose_name='Статус')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Full Name')
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name


class LogNewsLetter(models.Model):
    data_newsletter = models.DateTimeField(auto_now_add=True, verbose_name='Data Time Last Try')
    status_mailing = models.IntegerField(choices=StatusChoice.choices, default=StatusChoice.CREATED,
                                         verbose_name='Status')
    answer_server = models.TextField(verbose_name='Answer from Server')

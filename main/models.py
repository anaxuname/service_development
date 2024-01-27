from django.db import models


class StatusChoice(models.IntegerChoices):
    CREATED = 1, "CREATED"
    PROCESSING = 2, "PROCESSING"
    COMPLETED = 3, "COMPLETED"
    ERROR = 4, "ERROR"


class NewsLetter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name NewsLetter')
    time_mailing = models.TimeField(verbose_name='Time NewsLetter')
    periodicity_mailing = models.CharField(max_length=50, verbose_name='Periodicity')
    status_mailing = models.IntegerField(choices=StatusChoice.choices, default=StatusChoice.CREATED,
                                         verbose_name='Status')

    def __str__(self):
        return self.name

class Message(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    body = models.TextField(verbose_name='Content')
    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE)

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

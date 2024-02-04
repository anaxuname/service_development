import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from main.models import Message, PeriodicityChoice, StatusChoice, Client

logger = logging.getLogger(__name__)


def send_newsletter_mail(message, clients):
    try:
        emails = [client.email for client in clients]
        send_mail(subject=message.title,
                  message=message.body,
                  from_email=settings.EMAIL_HOST_USER, recipient_list=emails, fail_silently=False, )
        message.status_mailing = StatusChoice.COMPLETED
        # save message with new status
        message.save()
    except Exception as e:
        logger.exception(e)
        message.status_mailing = StatusChoice.ERROR
        # save message with new status
        message.save()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        messages = Message.objects.filter(status_mailing=StatusChoice.CREATED)
        for message in messages:
            clients = Client.objects.filter(newsletter=message.newsletter)
            if not clients:
                continue

            message.status_mailing = StatusChoice.PROCESSING
            message.save()

            if message.newsletter.periodicity_mailing == PeriodicityChoice.EVERY_DAY:
                scheduler.add_job(send_newsletter_mail, args=[message, clients],
                                  trigger=CronTrigger(second=message.newsletter.time_mailing.second,
                                                      minute=message.newsletter.time_mailing.minute,
                                                      hour=message.newsletter.time_mailing.hour),
                                  id=str(message.id) + '_message',
                                  max_instances=1, replace_existing=True, )
            elif message.newsletter.periodicity_mailing == PeriodicityChoice.EVERY_WEEK:
                scheduler.add_job(send_newsletter_mail, args=[message, clients],
                                  trigger=CronTrigger(second=message.newsletter.time_mailing.second,
                                                      minute=message.newsletter.time_mailing.minute,
                                                      hour=message.newsletter.time_mailing.hour, day_of_week=1, ),
                                  id=str(message.id) + '_message', max_instances=1, replace_existing=True, )
            elif message.newsletter.periodicity_mailing == PeriodicityChoice.EVERY_MONTH:
                scheduler.add_job(send_newsletter_mail, args=[message, clients],
                                  trigger=CronTrigger(second=message.newsletter.time_mailing.second,
                                                      minute=message.newsletter.time_mailing.minute,
                                                      hour=message.newsletter.time_mailing.hour, day=1, ),
                                  id=str(message.id) + '_message',
                                  max_instances=1, replace_existing=True, )

        scheduler.add_job(delete_old_job_executions, trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
                          # Midnight on Monday, before start of the next work week.
                          id="delete_old_job_executions", max_instances=1, replace_existing=True, )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

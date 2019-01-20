import datetime
from django.utils import timezone

from django.http import HttpResponse, HttpResponseForbidden
from django.views import View

from accounts.models import Account, Category, Reminder, RecurringReminder
from spero.utils import notify_on_reminder


# Create your views here.


class CheckAccountTask(View):

    def get(self, request):
        try:
            if not request.META['HTTP_X_APPENGINE_CRON']:
                return HttpResponseForbidden('Must be called from GAE cron')
        except KeyError:
            return HttpResponseForbidden('Must be called from GAE cron')
        two_weeks_ago = timezone.now().date() - datetime.timedelta(days=14)
        accounts = Account.objects.filter(logentry__modified__date=two_weeks_ago).\
            exclude(created__gt=two_weeks_ago).exclude(active=False)
        category = Category.objects.filter(name__icontains="other").first()
        for account in accounts:
            already_checked = False
            reminders = account.reminder_set.filter(log_entry__isnull=False)
            for reminder in reminders:
                if reminder.title == "Check account":
                    already_checked = True
                    break
            if already_checked:
                continue
            reminder = Reminder.objects.create(
                title="Check account",
                category=category,
                alert_time=datetime.date.today(),
                is_todo=False,
                account=account,
            )
            reminder.save()
            notify_on_reminder(reminder)
        return HttpResponse("Reminders created successfully")


class CheckRecurringReminderTask(View):

    def get(self, request):
        today = datetime.date.today()
        try:
            if not request.META['HTTP_X_APPENGINE_CRON']:
                return HttpResponseForbidden('Must be called from GAE cron')
        except KeyError:
            return HttpResponseForbidden('Must be called from GAE cron')
        recurring_reminders = RecurringReminder.objects.filter(account__active=True)
        for recurring_reminder in recurring_reminders:
            if (
                    recurring_reminder.interval == "W"
                    and today.isoweekday() == recurring_reminder.day
            ) or (
                    recurring_reminder.interval == "F"
                    and today.isoweekday() == recurring_reminder.day
                    and (recurring_reminder.last_reminded is None
                         or today - datetime.timedelta(days=8) > recurring_reminder.last_reminded)
            ) or (
                    recurring_reminder.interval == "M"
                    and today.day == recurring_reminder.day
            ):
                reminder = Reminder.objects.create(
                    title=recurring_reminder.title,
                    category=recurring_reminder.category,
                    alert_time=today,
                    is_todo=False,
                    account=recurring_reminder.account,
                )
                reminder.save()
                notify_on_reminder(reminder)
                recurring_reminder.last_reminded = timezone.now().date()
                recurring_reminder.save()
        return HttpResponse("Reminders created successfully")

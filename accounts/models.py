from django.db import models

from spero.mixins import DatesMixin

from authentication.models import User

# Create your models here.


class Customer(DatesMixin):
    """
    Customer model. This represents a customer who can have multiple accounts assigned to them.
    """
    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    # a customer user has the same access to all related accounts as an assigned user
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Account(DatesMixin):
    """
    This represents a marketing account.
    """
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    google_ads_id = models.CharField(max_length=50, null=True, blank=True)
    facebook_page = models.URLField(max_length=200, null=True, blank=True)
    google_analytics_id = models.CharField(max_length=50, null=True, blank=True)
    google_tag_manager_code = models.CharField(max_length=50, null=True, blank=True)
    search_monthly_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    assigned_users = models.ManyToManyField(User)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(DatesMixin):
    """
    This represents a category that can be used for reminders and log entries on an account.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Reminder(DatesMixin):
    """
    This is a reminder. It can be a to do or an alert.
    """
    title = models.CharField(max_length=500)
    alert_time = models.DateField(null=True, blank=True)
    is_todo = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.account.name}"

class RecurringReminder(DatesMixin):
    """
    This is a recurring reminder. This represents a pattern used to generate alerts by a cron job.
    """
    INTERVALS = (
        ('W', 'Weekly'),
        ('F', 'Fortnightly'),
        ('M', 'Monthly'),
    )
    MAX_DAY = 28

    title = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    interval = models.CharField(max_length=1, choices=INTERVALS)
    # day will be the day of the week (1 - 7) if interval is W or F and day of the month (1-28) if M.
    day = models.IntegerField(choices=[(i, i) for i in range(1, MAX_DAY + 1)])
    last_reminded = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} every {self.interval} on {self.day}"


class LogEntry(DatesMixin):
    """
    This represents a log entry for an account.
    The log entry can have an associated reminder (which clears that reminder if the log entry is
    not a draft) or not.
    """
    description = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    time_spent = models.DurationField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    draft = models.BooleanField()
    reminder = models.OneToOneField(Reminder, on_delete=models.PROTECT, null=True, blank=True, related_name="log_entry")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="log_entries")
    notify = models.BooleanField(default=False)
    notify_users = models.ManyToManyField(User, related_name="notify_log_entries", null=True, blank=True)

    def __str__(self):
        return self.description



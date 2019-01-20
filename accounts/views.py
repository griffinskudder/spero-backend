from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets

from spero.permissions import IsAuthenticatedOrOptions, \
    IsAdminUserOrAuthenticatedAndReadOnlyOrOptions
from spero.utils import notify_on_reminder
from .models import Account, Reminder, Category, LogEntry, Customer, RecurringReminder
from .serializers import AlertSerializer, ToDoSerializer, AccountSerializer, CategorySerializer, LogEntrySerializer, \
    CustomerSerializer, RecurringAlertSerializer


# Create your views here.


class AlertViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given alert (limited to alerts that the user has access to).
    list:
    Return all active alerts for accounts the user is assigned access to (active means no reminder is associated).
    create:
    Create a new alert instance.
    destroy:
    Deletes the specified alert instance.
    update:
    Update the specified alert instance.
    partial_update:
    Update the specified alert instance without requiring all fields.
    """
    queryset = Reminder.objects.none()
    serializer_class = AlertSerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        # TODO: this query is ridiculous. Profile it.
        return Reminder.objects.filter(is_todo=False, alert_time__lte=timezone.now(),
                                       account__active=True). \
            filter(Q(log_entry__isnull=True) | Q(log_entry__draft=True)). \
            filter(Q(account_id__in=user.account_set.all()) |
                   Q(account__customer_id__in=user.customer_set.all())). \
            order_by('alert_time')

    def perform_create(self, serializer):
        instance = serializer.save()
        notify_on_reminder(instance, self.request.user)


class FutureAlertViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given future alert (limited to future alerts that the user has access to).
    list:
    Return all future alerts for accounts the user is assigned access to (future alert means that the alert has a future date).
    """
    queryset = Reminder.objects.none()
    serializer_class = AlertSerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        # TODO: this query is ridiculous. Profile it.
        return Reminder.objects.filter(is_todo=False, alert_time__gt=timezone.now(),
                                       account__active=True). \
            filter(Q(log_entry__isnull=True) | Q(log_entry__draft=True)). \
            filter(Q(account_id__in=user.account_set.all()) |
                   Q(account__customer_id__in=user.customer_set.all())). \
            order_by('alert_time')


class CustomerViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get the specified customer
    list:
    Get all customers
    create:
    Create a new customer instance
    destroy:
    Delete the specified customer instance
    update:
    Update the specified customer instance
    partial_update
    Update the specified customer instance without requiring all fields.
    """
    queryset = Customer.objects.none()

    serializer_class = CustomerSerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Customer.objects.all().order_by('name')
        else:
            return user.customer_set.all().order_by('name')


class ToDoViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given to do (limited to to dos that the user has access to).
    list:
    Return all active to dos for accounts the user is assigned access to (active means no reminder is associated).
    create:
    Create a new to do instance.
    destroy:
    Deletes the specified to do instance.
    update:
    Update the specified to do instance.
    partial_update:
    Update the specified to do instance without requiring all fields.
    """
    queryset = Reminder.objects.none()
    serializer_class = ToDoSerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        # TODO: this query is ridiculous. Profile it.
        return Reminder.objects.filter(is_todo=True,
                                       account__active=True). \
            filter(Q(log_entry__isnull=True) | Q(log_entry__draft=True)). \
            filter(Q(account_id__in=user.account_set.all()) |
                   Q(account__customer_id__in=user.customer_set.all()))

    def perform_create(self, serializer):
        instance = serializer.save()
        notify_on_reminder(instance, self.request.user)


class ReminderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given reminder (limited to reminders that the user has access to).
    list:
    Return all reminders for accounts the user is assigned access to.
    """
    queryset = Reminder.objects.none()

    serializer_class = AlertSerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        return Reminder.objects.filter(Q(account__id__in=user.account_set.all()) |
                                       Q(account__customer_id__in=user.customer_set.all()))


class ActiveReminderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given reminder (limited to reminders that the user has access to).
    list:
    Return all active reminders for accounts and customers the user is assigned access to.
    """
    queryset = Reminder.objects.none()

    serializer_class = AlertSerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        return Reminder.objects.filter(account__active=True). \
            filter(Q(is_todo=True) |
                   Q(alert_time__lte=timezone.now())). \
            filter(Q(log_entry__isnull=True) |
                   Q(log_entry__draft=True)). \
            filter(Q(account__id__in=user.account_set.all()) |
                   Q(account__customer_id__in=user.customer_set.all()))


class RecurringReminderViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get the specified recurring reminder (user must have access)
    list:
    Get all recurring reminders that the user has access to.
    create:
    Create a new recurring reminder
    destroy:
    Delete the specified recurring reminder
    update:
    Update the specified recurring reminder
    partial_update
    Update the specified recurring reminder instance without requiring all fields.
    """
    queryset = RecurringReminder.objects.none()

    serializer_class = RecurringAlertSerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        return RecurringReminder.objects.filter(Q(account__id__in=user.account_set.all()) |
                                                Q(account__customer_id__in=user.customer_set.all()))


class AccountViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get the specified account(user must have access)
    list:
    Get all accounts that the user has access to.
    create:
    Create a new account
    destroy:
    Delete the specified account
    update:
    Update the specified account
    partial_update
    Update the specified account instance without requiring all fields.
    """
    queryset = Account.objects.none()
    serializer_class = AccountSerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        queryset = Account.objects.filter(customer_id__in=user.customer_set.all()) | user.account_set.all()
        return queryset.order_by('name')


class CategoryViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get the specified category(user must be admin)
    list:
    Get all categories that the user has access to.
    create:
    Create a new category
    destroy:
    Delete the specified category
    update:
    Update the specified category
    partial_update
    Update the specified category instance without requiring all fields.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer

    permission_classes = [IsAdminUserOrAuthenticatedAndReadOnlyOrOptions]


class LogEntryViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Get the specified log entry(user must have access)
    list:
    Get all log entries that the user has access to.
    create:
    Create a new log entry
    destroy:
    Delete the specified log entry
    update:
    Update the specified log entry
    partial_update
    Update the specified log entry instance without requiring all fields.
    """
    queryset = LogEntry.objects.none()
    serializer_class = LogEntrySerializer

    permission_classes = [IsAuthenticatedOrOptions]

    def get_queryset(self):
        user = self.request.user
        return LogEntry.objects.filter(Q(account_id__in=user.account_set.all()) |
                                       Q(account__customer_id__in=user.customer_set.all())). \
            order_by('-modified')

    def perform_create(self, serializer):
        instance = serializer.save()
        if (
                not instance.draft
                and instance.notify
        ):
            reminder = Reminder.objects.create(
                title=instance.description[0:501],
                alert_time=timezone.now(),
                is_todo=False,
                category=instance.category,
                account=instance.account
            )
            notify_on_reminder(reminder, self.request.user)

    def perform_update(self, serializer):
        old_instance = self.get_object()
        new_instance = serializer.save()
        if (not old_instance.draft
                and new_instance.draft
                and new_instance.notify
        ):
            reminder = Reminder.objects.create(
                title=new_instance.description[0:501],
                alert_time=timezone.now(),
                is_todo=False,
                category=new_instance.category,
                account=new_instance.account
            )
            notify_on_reminder(reminder, self.request.user)

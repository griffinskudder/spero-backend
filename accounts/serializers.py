from rest_framework import serializers

from .models import Customer, Account, Category, Reminder, LogEntry, RecurringReminder


class AlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reminder
        fields = ('id', 'title', 'alert_time', 'is_todo', 'category', 'account', 'log_entry')
        read_only_fields = ('log_entry',)


class ToDoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reminder
        fields = ('id', 'title', 'is_todo', 'category', 'account', 'log_entry')
        read_only_fields = ('log_entry',)


class RecurringAlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecurringReminder
        fields = ('id', 'title', 'category', 'account', 'interval', 'day')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'notes', 'account_set', 'users')
        read_only_fields = ('account_set',)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'name', 'customer',
                  'url', 'google_ads_id',
                  'facebook_page',
                  'google_analytics_id',
                  'google_tag_manager_code',
                  'search_monthly_budget',
                  'assigned_users', 'notes')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ('id', 'description', 'category', 'draft',
                  'time_spent', 'account', 'reminder', 'modified',
                  'created_by', 'notify', 'notify_users')

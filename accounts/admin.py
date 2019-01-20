from django.contrib import admin

from .models import Customer, Account, Category, Reminder, RecurringReminder, LogEntry

# Register your models here.

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Reminder)
admin.site.register(RecurringReminder)
admin.site.register(LogEntry)

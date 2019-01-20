"""
Utility functions
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from spero.settings import EMAIL_FROM_ADDRESS


def notify_on_reminder(reminder, created_by=None):
    """

    :param reminder: The newly created reminder to notify on
    :param created_by: Default None, should be left at default only if the reminder was created by the system
    :return: None
    """
    if created_by is not None:
        notify_users = reminder.account.assigned_users.exclude(id=created_by.id)
        created_by_name = f"{created_by.first_name} {created_by.last_name}"
    else:
        notify_users = reminder.account.assigned_users.all()
        created_by_name = "System"
    account_name = reminder.account.name
    for user in notify_users:
        # TODO: format the message body properly.
        message = EmailMultiAlternatives(
            f"A new reminder has been created on {account_name}",
            render_to_string('remindernotifyemail.txt', {'user': user,
                                                         'account_name': account_name,
                                                         'created_by_name': created_by_name,
                                                         'reminder': reminder}
                             ),
            EMAIL_FROM_ADDRESS,
            [f"{user.first_name} {user.last_name}<{user.email}>"]
        )
        message.attach_alternative(render_to_string('remindernotifyemail.html', {'user': user,
                                                                                 'account_name': account_name,
                                                                                 'created_by_name': created_by_name,
                                                                                 'reminder': reminder}
                                                    ),
                                   "text/html")
        message.send(fail_silently=True)

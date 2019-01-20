"""Spero URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from accounts.views import AlertViewSet, LogEntryViewSet, AccountViewSet, CategoryViewSet, ToDoViewSet, \
    CustomerViewSet, ReminderViewSet, FutureAlertViewSet, RecurringReminderViewSet, ActiveReminderViewSet
from authentication.views import UserViewSet, CurrentUserViewSet
from tasks.views import CheckAccountTask, CheckRecurringReminderTask
from spero.views import LoginView, LogoutView

from knox import views as knox_views
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

auth_router = DefaultRouter()

auth_router.register('user', UserViewSet)
auth_router.register('current_user', CurrentUserViewSet)

accounts_router = DefaultRouter()

accounts_router.register('alert', AlertViewSet)
accounts_router.register('future_alert', FutureAlertViewSet)
accounts_router.register('todo', ToDoViewSet)
accounts_router.register('log_entry', LogEntryViewSet)
accounts_router.register('customer', CustomerViewSet)
accounts_router.register('account', AccountViewSet)
accounts_router.register('category', CategoryViewSet)
accounts_router.register('reminder', ReminderViewSet)
accounts_router.register('active_reminder', ActiveReminderViewSet)
accounts_router.register('recurring_reminder', RecurringReminderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'tasks/check_account/', CheckAccountTask.as_view(), name='check_account'),
    re_path(r'tasks/recurring_reminders/', CheckRecurringReminderTask.as_view(), name='recurring_reminder'),
    re_path(r'api/auth/login/', LoginView.as_view(), name='knox_login'),
    re_path(r'api/auth/logout/', LogoutView.as_view(), name='knox_logout'),
    re_path(r'api/auth/logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('api/v1/auth/', include(auth_router.urls)),
    path('api-authentication/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/accounts/', include(accounts_router.urls)),
    re_path(r'^docs/', include_docs_urls(title='Account Management Platform API')),
    re_path('.*', TemplateView.as_view(template_name='index.html')),
]

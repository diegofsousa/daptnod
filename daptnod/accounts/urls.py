from django.conf.urls import url
from django.urls import path, include
from .views import login, logout, RegisterView, UpdateUserView, UpdatePasswordView, me, offer_retry_sending_email, retry_sending_email

app_name = 'accounts'

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('signup', RegisterView.as_view(), name='signup'),
    path('signup/activation', offer_retry_sending_email, name='offer_retry_sending_email'),
    path('signup/activation/retry_send_email', retry_sending_email, name='retry_sending_email'),
    path('settings', me, name='settings'),
    path('settings/edit', UpdateUserView.as_view(), name='edit'),
    path('settings/change_password', UpdatePasswordView.as_view(), name='change_password'),
]
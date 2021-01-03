from django.conf.urls import url
from django.urls import path, include
from .views import login, logout, RegisterView, UpdateUserView, UpdatePasswordView, me

app_name = 'accounts'

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('signup', RegisterView.as_view(), name='signup'),
    path('settings', me, name='settings'),
    path('settings/edit', UpdateUserView.as_view(), name='edit'),
    path('settings/change_password', UpdatePasswordView.as_view(), name='change_password'),
]
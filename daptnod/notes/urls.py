from django.conf.urls import url
from django.urls import path, include
from .views import index


app_name = 'notes'

urlpatterns = [
    path('', index, name='index')
]
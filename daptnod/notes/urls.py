from django.conf.urls import url
from django.urls import path, include
from .views import index, create_note, note


app_name = 'notes'

urlpatterns = [
	path('', index, name='index'),
	path('new', create_note, name='new'),
	path('<str:hashid>', note, name='note')
]
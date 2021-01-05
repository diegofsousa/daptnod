from django.conf.urls import url
from django.urls import path, include
from .views import index, create_note, note, blocking_or_unblocking_note, private_or_public_note


app_name = 'notes'

urlpatterns = [
	path('', index, name='index'),
	path('new', create_note, name='new'),
	path('<str:hashid>', note, name='note'),
	path('<str:hashid>/lock', blocking_or_unblocking_note, name='note_lock'),
	path('<str:hashid>/private', private_or_public_note, name='note_private')
]
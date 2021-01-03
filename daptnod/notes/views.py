from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Note
from django.utils import timezone
import json

def index(request):
	login_error = request.session.get('login_error', None)
	request.session['login_error'] = None
	return render(request, 'index.html', {
		'login_error':login_error
	})

def create_note(request):
	# 1° caso é quando ele é anonimo
	if request.user.is_authenticated == False:
		note = Note()
		note.save()
		return redirect('notes:note', hashid=note.id.hashid)

def note(request, hashid):
	note = get_object_or_404(Note, id=hashid)
	if request.user.is_authenticated == False:
		if request.method == 'POST':
			handler_update_note_by_anonymous(request, note)
			return HttpResponse(json.dumps(True), content_type="application/json")
		note.views_number = note.views_number + 1
		note.save()
		return render(request, 'note.html', {
			'data':note
		})

def handler_update_note_by_anonymous(request, note):
		note.updated_at = timezone.now()
		note.updated_by = None
		note.content = request.POST.get('content')
		note.save()
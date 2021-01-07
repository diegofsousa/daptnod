from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q
from .models import Note
from django.utils import timezone
import json

def index(request):
	login_error = request.session.get('login_error', None)
	request.session['login_error'] = None
	if request.user.is_authenticated:
		my_notes = Note.objects.filter(created_by__pk=request.user.pk)[:10]
		recent_changes = Note.objects.filter(viewers__pk=request.user.pk)[:10]

		return render(request, 'index_authenticated.html', {
			'login_error': login_error,
			'my_notes': my_notes,
			'recent_changes': recent_changes
		})
	else:
		return render(request, 'index.html', {
			'login_error':login_error
		})

def create_note(request):
	# 1° caso é quando ele é anonimo
	if request.user.is_authenticated == False:
		note = Note()
		note.save()
	else:
		note = Note()
		note.created_by = request.user
		note.updated_by = request.user
		note.is_anonymous = False
		note.save()
	return redirect('notes:note', hashid=note.id.hashid)

def note(request, hashid):
	note = get_object_or_404(Note, id=hashid)

	if request.user.is_authenticated == False:
		if note.is_private:
			raise PermissionDenied

		if request.method == 'POST':
			handler_update_note_by_anonymous(request, note)
			return HttpResponse(json.dumps(True), content_type="application/json")
		
		Note.objects.filter(pk=note.pk).update(views_number=note.views_number + 1)
		
		return render(request, 'note.html', {
			'data':note
		})
	else:
		if note.is_private and note.created_by_id != request.user.pk:
			raise PermissionDenied

		if request.method == 'POST':
			if note.is_locked == True:
				return HttpResponse(json.dumps(False), content_type="application/json")
			handler_update_note_by_authenticated_user(request, note)
			return HttpResponse(json.dumps(True), content_type="application/json")

		if Note.objects.filter(pk=note.pk, viewers__pk=request.user.pk).exists() == False:
			note.viewers.add(request.user)

		if request.user.pk != note.created_by_id or note.views_number == 0:
			Note.objects.filter(pk=note.pk).update(views_number=note.views_number + 1)

		return render(request, 'note.html', {
			'data':note,
			'show_menus':request.user.pk == note.created_by_id
		})

def handler_update_note_by_anonymous(request, note):
	Note.objects.filter(pk=note.pk).update(
		updated_at = timezone.now(),
		updated_by = None,
		content = request.POST.get('content')
	)

def handler_update_note_by_authenticated_user(request, note):
	Note.objects.filter(pk=note.pk).update(
		updated_at = timezone.now(),
		updated_by = request.user,
		content = request.POST.get('content')
	)

def blocking_or_unblocking_note(request, hashid):
	note = get_object_or_404(Note, id=hashid)

	if note.created_by_id != request.user.pk:
		raise PermissionDenied

	Note.objects.filter(pk=note.pk).update(is_locked=not note.is_locked)
	messages.success(request, 'The content blocking settings have been successfully made!')
	return redirect('notes:note', hashid=note.id.hashid)

def private_or_public_note(request, hashid):
	note = get_object_or_404(Note, id=hashid)

	if note.created_by_id != request.user.pk:
		raise PermissionDenied

	Note.objects.filter(pk=note.pk).update(is_private=not note.is_private)
	messages.success(request, 'Content privacy settings have been successfully made!')
	return redirect('notes:note', hashid=note.id.hashid)

class MyNotesList(ListView):
	model = Note
	http_method_names = ['get']
	template_name = 'list/my_notes.html'
	context_object_name = 'notes'
	paginate_by = 7

	def get_queryset(self):
		self.queryset = super().get_queryset().filter(created_by__pk=self.request.user.pk)
		if self.request.GET.get('search_box', False):
			self.queryset=self.queryset.filter(Q(content__icontains = self.request.GET['search_box']))
		return self.queryset
	
	def get_context_data(self, **kwargs):
		_super = super()
		context = _super.get_context_data(**kwargs)
		adjacent_pages = 3
		page_number = context['page_obj'].number
		num_pages = context['paginator'].num_pages
		startPage = max(page_number - adjacent_pages, 1)
		if startPage <= 5:
			startPage = 1
		endPage = page_number + adjacent_pages + 1
		if endPage >= num_pages - 1:
			endPage = num_pages + 1
		page_numbers = [n for n in range(startPage, endPage) \
				if n > 0 and n <= num_pages]
		context.update({
			'page_numbers': page_numbers,
			'show_first': 1 not in page_numbers,
			'show_last': num_pages not in page_numbers,
			})

		return context

class RecentChangesList(ListView):
	model = Note
	http_method_names = ['get']
	template_name = 'list/recent_changes.html'
	context_object_name = 'notes'
	paginate_by = 7

	def get_queryset(self):
		self.queryset = super().get_queryset().filter(viewers__pk=self.request.user.pk)
		if self.request.GET.get('search_box', False):
			self.queryset=self.queryset.filter(Q(content__icontains = self.request.GET['search_box']))
		return self.queryset
	
	def get_context_data(self, **kwargs):
		_super = super()
		context = _super.get_context_data(**kwargs)
		adjacent_pages = 3
		page_number = context['page_obj'].number
		num_pages = context['paginator'].num_pages
		startPage = max(page_number - adjacent_pages, 1)
		if startPage <= 5:
			startPage = 1
		endPage = page_number + adjacent_pages + 1
		if endPage >= num_pages - 1:
			endPage = num_pages + 1
		page_numbers = [n for n in range(startPage, endPage) \
				if n > 0 and n <= num_pages]
		context.update({
			'page_numbers': page_numbers,
			'show_first': 1 not in page_numbers,
			'show_last': num_pages not in page_numbers,
			})

		return context
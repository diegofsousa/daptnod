from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import HttpResponse, Http404, redirect

def login(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user is not None:
			if user.is_active:
				django_login(request, user)
				return redirect('notes:index')
		request.session['login_error'] = True
		return redirect('notes:index')
	raise Http404

def logout(request):
	django_logout(request)
	return redirect('notes:index')
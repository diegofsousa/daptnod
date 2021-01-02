from django.shortcuts import render

def index(request):
  login_error = request.session.get('login_error', None)
  request.session['login_error'] = None
  return render(request, 'index.html', {
    'login_error':login_error
  })

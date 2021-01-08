from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import HttpResponse, Http404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserCreationForm, UpdateUserForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages

def login(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user is not None:
			if user.is_active:
				django_login(request, user)
				messages.warning(request, 'DAPTNOD is an experimental tool. We do not encourage you to keep important or secret information like logins and passwords.')
				return redirect('notes:index')
		request.session['login_error'] = True
		return redirect('notes:index')
	raise Http404

def logout(request):
	django_logout(request)
	return redirect('notes:index')

class RegisterView(SuccessMessageMixin, CreateView):

	model = User
	template_name = 'register.html'
	form_class = UserCreationForm
	success_message = "Yay! You have been successfully registered. Login to DAPTNOD."
	success_url = reverse_lazy('notes:index')

@login_required
def me(request):
	return render(request, 'detail.html')

class UpdateUserView(LoginRequiredMixin, UpdateView):

	model = User
	form_class = UpdateUserForm
	template_name = 'update_user.html'
	success_url = reverse_lazy('accounts:settings')


	def post(self, request, *args, **kwargs):

		self.object = self.get_object()
		form = self.form_class(
			self.request.POST, instance=self.object)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_object(self):
		return self.request.user

	def form_valid(self, form):
		form.save()
		messages.success(self.request, 'Updated user registration.')
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form
			)
		)

	def get_success_url(self):
		return reverse('accounts:settings')

class UpdatePasswordView(LoginRequiredMixin, FormView):

	template_name = 'update_password.html'
	success_url = reverse_lazy('accounts:settings')
	form_class = PasswordChangeForm

	def get_form_kwargs(self):
		kwargs = super(UpdatePasswordView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form.save()
		messages.success(self.request, 'Updated password. Enter your new credentials to sign in.')
		return super(UpdatePasswordView, self).form_valid(form)
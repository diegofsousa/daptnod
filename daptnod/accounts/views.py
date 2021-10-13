from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import HttpResponse, Http404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from daptnod.commons.email import handler as email_handler
from .forms import UserCreationForm, UpdateUserForm
from .models import ActivationHash
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from datetime import timedelta

SECONDS_TO_TRY_AGAIN_ACTIVATION_EMAIL_REGISTER = 30
TOTAL_SECONDS_TO_ACTIVATION_CODE = 60 * 5
DAYS_TO_UNLOCK_EMAIL_ACTIVATION = 10
NUMBER_OF_ACTIVATION_ATTEMPTS_ALLOWED_WITHIN_THE_TIME_LIMIT = 3

def login(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user is not None:
			if user.is_active:
				django_login(request, user)
				messages.warning(request, 'DAPTNOD is an experimental tool. We do not encourage you to keep important or secret information like logins and passwords.')
				return redirect('notes:index')
			else:
				query_activation_links = ActivationHash.objects.filter(
					created_by__email = user.email,
					activated_at = None,
					created_at__gte=timezone.now() - timedelta(days=DAYS_TO_UNLOCK_EMAIL_ACTIVATION)	
				)

				request.session['email_user'] = user.email

				if query_activation_links.exists():
					return redirect('accounts:retry_sending_email')

				request.session['blocked_attempts'] = False
				
				activation_hash = ActivationHash()
				activation_hash.created_by = user
				activation_hash.save()

				email_handler.email_verification(user.username, user.email, activation_hash.hash_for_link_activation)

				return redirect('accounts:offer_retry_sending_email')

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

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()

		activation_hash = ActivationHash()
		activation_hash.created_by = user
		activation_hash.save()

		email_handler.email_verification(user.username, user.email, activation_hash.hash_for_link_activation)

		self.request.session['blocked_attempts'] = False
		self.request.session['email_user'] = user.email

		return redirect('accounts:offer_retry_sending_email')

def offer_retry_sending_email(request):
	email_user = request.session.get('email_user', None)

	if email_user != None and email_user != "":
		blocked_attempts = request.session.get('blocked_attempts', False)
		return render(request, 'retry_send_email_activation.html', {
			"email_user":email_user,
			"blocked_attempts":blocked_attempts
		})
	raise Http404

def retry_sending_email(request):
	email_user = request.session.get('email_user', None)

	if email_user != None and email_user != "":
		query_activation_links = ActivationHash.objects.filter(
			created_by__email = email_user,
			activated_at = None,
			created_at__gte=timezone.now() - timedelta(days=DAYS_TO_UNLOCK_EMAIL_ACTIVATION)	
		)

		if query_activation_links.exists():
			if query_activation_links.count() < NUMBER_OF_ACTIVATION_ATTEMPTS_ALLOWED_WITHIN_THE_TIME_LIMIT:
				first_result_query = query_activation_links[0]

				if (timezone.now() - first_result_query.created_at).total_seconds() >= SECONDS_TO_TRY_AGAIN_ACTIVATION_EMAIL_REGISTER:
					activation_hash = ActivationHash()
					activation_hash.created_by = first_result_query.created_by
					activation_hash.save()

					if query_activation_links.count() >= NUMBER_OF_ACTIVATION_ATTEMPTS_ALLOWED_WITHIN_THE_TIME_LIMIT:
						messages.warning(request, 'This is your last chance. You have been blocked for {} days from sending email on account activation.'.format(DAYS_TO_UNLOCK_EMAIL_ACTIVATION))
						request.session['blocked_attempts'] = True

					email_handler.email_verification(activation_hash.created_by.username, email_user, activation_hash.hash_for_link_activation)

					messages.info(request, 'A new activation link was sent to the registered email.')
					request.session['email_user'] = email_user

					return redirect('accounts:offer_retry_sending_email')
				else:
					messages.warning(request, 'Please wait {} seconds for the next attempt to activate by email.'.format(SECONDS_TO_TRY_AGAIN_ACTIVATION_EMAIL_REGISTER))
			else:
				messages.warning(request, 'You have been blocked for {} days from sending email on account activation.'.format(DAYS_TO_UNLOCK_EMAIL_ACTIVATION))
			return redirect('notes:index')
	raise PermissionDenied
	


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
		disable_user = False
		username = User.objects.get(pk=self.request.user.pk).username
		first_email = User.objects.get(pk=self.request.user.pk).email

		if first_email != form.cleaned_data['email']:
			email_handler.email_changed_notification(username, first_email, form.cleaned_data['email'])
			disable_user = True
		form.save()

		if disable_user == True:
			self.request.user.is_active = False
			self.request.user.save()
			messages.warning(self.request, 'Updated user information. You must Login again to activate the new email.')
			logout(self.request)
		else:
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

def activation_account(request, hashlink):
	activation_hash = get_object_or_404(ActivationHash, hash_for_link_activation=hashlink)
	if (timezone.now() - activation_hash.created_at).total_seconds() <= TOTAL_SECONDS_TO_ACTIVATION_CODE and activation_hash.activated_at == None:
		activation_hash.created_by.is_active = True
		activation_hash.created_by.save()

		activation_hash.activated_at = timezone.now()
		activation_hash.save()

		ActivationHash.objects.filter(
			created_by__pk = activation_hash.created_by.pk,
			activated_at = None
		).delete()

		messages.success(request, 'User activated successfully! To proceed, login with username and password.')
		return redirect('notes:index')
	
	raise Http404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserCreationForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['username', 'email']

class UpdateUserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username', 'email']
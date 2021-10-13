from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db.models import Q

class ModelBackend(BaseBackend):

	def authenticate(self, request, username=None, password=None):
		if not username is None:
			users = User.objects.filter(Q(email=username) | Q(username=username))
			if users.exists():
				user = users.first()
				if user.check_password(password):
					return user


	def get_user(self, user_id):
			try:
					return User.objects.get(pk=user_id)
			except User.DoesNotExist:
					return None
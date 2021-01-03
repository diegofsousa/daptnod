from django.db import models
from django.utils import timezone
from hashid_field import HashidAutoField
from django.contrib.auth.models import User

class Note(models.Model):
	id = HashidAutoField(primary_key=True)
	content = models.TextField(verbose_name='Content', null=False, blank=False, default='')
	is_anonymous = models.BooleanField(verbose_name='Is Anonymous', null=False, blank=False, default=True)
	created_at = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User, verbose_name='Created by', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
	updated_at = models.DateTimeField(default=timezone.now)
	updated_by = models.ForeignKey(User, verbose_name='Updated by', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
	viewers = models.ManyToManyField(User, verbose_name='Viewers', blank=True, related_name='+')
	views_number = models.IntegerField(verbose_name='Views number', null=False, blank=False, default=0)
	is_private = models.BooleanField(verbose_name="Is private", null=False, blank=False, default=False)
	is_locked = models.BooleanField(verbose_name="Is locked", null=False, blank=False, default=False)

	def __str__(self):
		return self.content[0:10]


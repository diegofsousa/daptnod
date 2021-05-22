from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from uuid import uuid4


User._meta.get_field('email')._unique = True

class ActivationHash(models.Model):
	created_at = models.DateTimeField(default=timezone.now)
	created_by = models.ForeignKey(User, verbose_name='Created by', related_name='+', on_delete=models.CASCADE)
	hash_for_link_activation = models.CharField(verbose_name='Hashlink', max_length=80)
	activated_at = models.DateTimeField(verbose_name='Activated at',null=True, blank=True)

	class Meta:
		verbose_name = 'ActivationHash'
		verbose_name_plural = 'ActivationHashes'
		ordering = ['-created_at']

	def save(self, *args, **kwargs):
		if self.hash_for_link_activation == None or self.hash_for_link_activation == "":
			self.hash_for_link_activation = generate_uuid_str()
		super(ActivationHash, self).save(*args, **kwargs)

	def __str__(self):
		return "Activation link to '{}'".format(self.created_by.email)

def generate_uuid_str():
	return str(uuid4())
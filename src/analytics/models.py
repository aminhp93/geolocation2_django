from django.db import models
from django.conf import settings

from .signals import user_logged_in

# Create your models here.
class UserSession(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL)
	session_key = models.CharField(max_length=60, null=True, blank=True)
	ip_address 	= models.GenericIPAddressField(null=True, blank=True)
	city_data 	= models.TextField(null=True, blank=True)
	city 		= models.CharField(max_length=120, null=True, blank=True)
	country 	= models.CharField(max_length=120, null=True, blank=True)
	active		= models.BooleanField(default=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if self.city_data:
			return str(self.city_data)
		return self.user.username

def user_logged_in_receiver(sender, request, *args, **kargs):
	user = sender
	print(user)
	print(request)
	print(request.session)
	session_key = request.session.session_key
	UserSession.objects.create(user=user, session_key=session_key)

	# UserSession.objects.create()	


user_logged_in.connect(user_logged_in_receiver)
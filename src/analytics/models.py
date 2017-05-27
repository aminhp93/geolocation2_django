from django.db import models
from django.conf import settings

from .signals import user_logged_in
from .utils import get_client_city_data, get_client_ip

# Create your models here.
class UserSessionManager(models.Manager):
	def create_new(self, user, session_key=None, ip_address=None):
		session_new = self.model()
		session_new.user = user
		session_new.session_key = session_key

		if ip_address is not None:
			session_new.ip_address = ip_address
			city_data = get_client_city_data(ip_address)
			session_new.city_data = city_data

			try:
				city = city_data["city"]
			except:
				city = None
			session_new.city = city

			try:
				country = city_data["country_name"]
			except:
				country = None
			session_new.country = country
			session_new.save()
			return session_new
		return None

class UserSession(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL)
	session_key = models.CharField(max_length=60, null=True, blank=True)
	ip_address 	= models.GenericIPAddressField(null=True, blank=True)
	city_data 	= models.TextField(null=True, blank=True)
	city 		= models.CharField(max_length=120, null=True, blank=True)
	country 	= models.CharField(max_length=120, null=True, blank=True)
	active		= models.BooleanField(default=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	objects = UserSessionManager()

	def __str__(self):
		city = self.city
		country = self.country
		if city and country:
			return "{}, {}".format(city, country)
		elif city and not country:
			return "{}".format(city)
		elif country and not city:
			return "{}".format(country)
		return self.user.username

def user_logged_in_receiver(sender, request, *args, **kargs):
	user = sender
	print(user)
	print(request)
	print(request.session)
	ip_address = get_client_ip(request)
	# ip_address = '72.14.207.99'
	# if ip_address:
	# city_data = get_client_city_data(ip_address)
	session_key = request.session.session_key
	UserSession.objects.create_new(user=user, 
		session_key=session_key,
		ip_address=ip_address)

	# UserSession.objects.create()	


user_logged_in.connect(user_logged_in_receiver)
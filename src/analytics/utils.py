from django.contrib.gis.geoip2 import GeoIP2

def get_client_ip(request):
	print(request.META)
	x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get("REMOTE_ADDR")
	return ip

def get_client_city_data(ip_address):
	g = GeoIP2()
	try:
		return g.city(ip_address)
	except:
		return None

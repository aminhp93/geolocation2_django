import datetime
import requests
from django.conf import settings

from django.utils import timezone

YELP_AUTH_ENDPOINT = 'https://api.yelp.com/oauth2/token'
YELP_SEARCH_ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
YELP_CLIENT_ID = getattr(settings, 'YELP_CLIENT_ID','dE26izDXFldzCgO2QpNp3g')
YELP_CLIENT_SECRET = getattr(settings, 'YELP_CLIENT_SECRET','u81sucWSTOuRw0R2cBiY3ebRydCfNPDXlZIfz7Z5lEDrzIJtcM3GlGTp5iDpBjpF')

def get_token(request=None):
	token_exists = False
	if request:
		session_token = request.session.get('YELP_TOKEN')
		token_expires = request.session.get('YELP_EXPIRES')
		if session_token:
			token_exists = True
			token = session_token
	if not token_exists:
		params = {
			'grant_type': 'OAUTH2',
			'client_id': YELP_CLIENT_ID,
			'client_secret': YELP_CLIENT_SECRET
		}
		r = requests.post(YELP_AUTH_ENDPOINT, params=params)
		print(r.text)
		token = r.json()['access_token']
		expires = r.json()['expires_in']
		if request:
			request.session['YELP_TOKEN'] = token
			request.session['YELP_EXPIRES'] = timezone.now() + datetime.datetime(seconds=expires)
	return token

def yelp_search(keyword='Food', location='Newport Beach'):
	token = get_token()
	headers = {"Authorization": "Bearer " + token}
	params = {"term": keyword, "location": location}
	r = requests.get(YELP_SEARCH_ENDPOINT, headers=headers, params=params)
	print(r.status_code)
	return r.json()
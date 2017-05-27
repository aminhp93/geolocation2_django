from django.views.generic import View
from django.shortcuts import render

from .utils import yelp_search

# Create your views here.
class SearchView(View):
	def get(self, request, *args, **kawrgs):
		items = []
		q = request.GET.get('q')
		location = request.session.get('CITY', 'Newport Beach')
		print(location, "LOCATION")
		if q:
			items = yelp_search(keyword='some food', location=location, request=request)
		return render(request, 'search/home.html', {'result': items})
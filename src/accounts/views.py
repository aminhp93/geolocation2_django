from django.contrib.auth.views import LoginView as DefaultLoginView, LogoutView as DefaultLogoutView
from django.shortcuts import render
from analytics.signals import user_logged_in

from .forms import LoginForm
# Create your views here.

class LoginView(DefaultLoginView):
	authentication_form = LoginForm

	def form_valid(self, form):
		done_ = super().form_valid(form)
		print(form.cleaned_data)
		print(self.request)
		print(self.request.user)
		if self.request.user.is_authenticated:
			user_logged_in.send(self.request.user, request=self.request)
		return done_

class LogoutView(DefaultLogoutView):
	pass
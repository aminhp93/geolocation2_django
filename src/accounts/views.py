from django.contrib.auth.views import LoginView as DefaultLoginView
from django.shortcuts import render

from .forms import LoginForm
# Create your views here.

class LoginView(DefaultLoginView):
	authentication_form = LoginForm
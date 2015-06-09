from django.contrib.auth.views import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def account_change(request):
	return login(request,template_name='ajax/form_load.html')
	

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from forms import *

@login_required
def test_login(request):
	return render(request,'test_login.html')

from django.contrib.auth.models import User

def register(request):
	if request.method=='POST':
		form=MyUserCreationForm(request.POST)
		if form.is_valid():
			new_user=form.save()

			user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
			if user is not None and user.is_active:
				login(request,user)
			request.user.message_set.create(message=user.username+", Your registration have completed")
			return HttpResponseRedirect('/accounts/set_email/')
	else:
		form=MyUserCreationForm()
	return render(request,'register.html',{'form':form})

@login_required
def sitemap(request):
	return render(request,'sitemap.html')

@login_required
def set_email(request):
	if request.method=='POST':
		form=UserForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			return render(request,'set_email_done.html',{'email':form['email'].data})
	else:
		form=UserForm(instance=request.user)
	return render(request,'set_email.html',{'form':form})

#from forms import TestForm
#def test_form(request):
#	if request.method=='POST':
#		form=TestForm(request.POST)
#		if form.is_valid():
#			id=int(form['creater'].data)
#			instance=btest.objects.get(id=1)
#			instance.creater=User(id)
#			instance.save()
#	else:
#		form=TestForm()
#	return render_to_response('register.html',{'form':form})

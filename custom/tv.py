# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render_to_response, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import F


from custom.models import *
from custom.forms import *
from work import settings

def check_address(user,id):
	valid=True
	if valid and not id:
		valid=False
	if valid:
		set=Address.objects.filter(pk=id)
		if set.count()==0:
			valid=False
		if valid and set[0].user!=user:
			valid=False
	return valid

	
@login_required
def address(request,id=None):
	set=Address.objects.filter(user=request.user).order_by('-id')

	permit=set.count()<settings.MAX_ADDRESS_NUM

	if id:
		if not check_address(request.user,id):
			raise Http404
		if request.method=='POST':
			form=AddressForm(request.POST)
			if form.is_valid():
				addr=form.save(commit=False)
				addr.id=id
				addr.user=request.user
				addr.save()
				request.user.message_set.create(message='address have been updated')
				return HttpResponseRedirect('/address/')
		else:
			form=AddressForm(instance=Address.objects.get(pk=id))

	else:
		if request.method=='POST':
			if not permit:
				request.user.message_set.create(message='Your address book is full')
				form=AddressForm()
				form.non_field_errors()
			else:
				form=AddressForm(request.POST)
				if form.is_valid():
					addr=form.save(commit=False)
					addr.user=request.user
					addr.save()
					request.user.message_set.create(message='new address have been saved')
					return HttpResponseRedirect('/address/')
		else:
			form=AddressForm()

	return render(request,'address.html',{'form':form,'item':set,'permit':permit,'id':id})

@login_required
def address_del(request,id):
	if not check_address(request.user,id):
		raise Http404
	Address.objects.get(pk=id).delete()
	return HttpResponse('0')

def food(request,id):
	Menu.objects.filter(pk=id).update(click=F('click')+1)
	item=get_object_or_404(Menu, pk=id)
	return render(request,'food.html',{'item':item,'path':request.get_full_path()})

@login_required
def message(request,page=0,type=0):
	try:
		page=int(page)
	except ValueError:
		raise Http500
		pass

	set=Message.objects.filter(user=request.user,type=type)

	if type==0:
		set=set.filter(receiver=request.user).order_by('-date')
	elif type==1:
		set=set.filter(sender=request.user).order_by('-date')
	else:
		set=set.filter(sender=request.user).order_by('-date')

	start=page*settings.MESSAGE_PER_PAGE
	end=start+settings.MESSAGE_PER_PAGE

	items=set[start:end]

	max_page=(set.count()-1)/settings.MESSAGE_PER_PAGE


	if page!=0 and items.count()==0:
		raise Http404

	if type==0:
		url='/message/'
		title='Message:Inbox'
	elif type==1:
		url='/message/outbox/'
		title='Message:Outbox'
	else:
		url='/message/draft/'
		title='Draft box'

	return render(request,'message_display.html',{
		'items':items,
		'title':title,
		'type':type,
		'page_range':xrange(max_page+1),
		'url':url,
		'current':page,
	})

@login_required
def message_edit(request,id=None):
	draft=None
	if request.method=='POST':
		form=MessageForm(request.POST)
		draft=request.POST.get('draft')

		if form.is_valid():
			msg=form.save(commit=False)

			receiver=User.objects.get(username=form.cleaned_data['dst'])
			msg.receiver=receiver
			msg.sender=request.user
			msg.user=receiver
			msg.state=0
			msg.type=0
			# save to receiver's inbox
			msg.save()

			# save to sender's outbox
			msg.id=None
			msg.type=1
			msg.user=request.user
			msg.save()

			if draft:
				draft=Message.objects.filter(pk=draft)
				if draft.count()>0:
					draft=draft[0]
				if draft.type==2 and draft.user==request.user:
					draft.delete()

			return HttpResponseRedirect("/message/outbox/")
	elif id:
		set=Message.objects.filter(pk=id)
		if set.count()==0:
			raise Http404

		message=set[0]
		if message.user!=request.user:
			raise Http404

		if message.type==0:
			form=MessageForm(initial={'dst':message.sender.username,'title':'Re: '+message.title})
		elif message.type==2:
			form=MessageForm(instance=message)
			draft=message.id
		else:
			raise Http404
	else:
		form=MessageForm()

	return render(request,'message.html',{'form':form,'draft':draft})

@login_required
def message_del(request,id):
	set=Message.objects.filter(pk=id)
	if set.count()==0:
		raise Http404

	message=set[0]
	if message.user!=request.user:
		raise Http404

	message.delete()
	return HttpResponse('0');

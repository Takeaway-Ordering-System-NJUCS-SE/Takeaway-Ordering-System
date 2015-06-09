# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import F
from django.core.urlresolvers import reverse


from custom.models import *
from custom.forms import *


import datetime
import copy

############################shortcuts for shortcuts
rento=render_to_response
httpr=HttpResponse

############################constant
#order states
unfinished 	= 0
committed 	= 1
paid 		= 2
cooking 	= 3
delivering 	= 4
finished 	= 5
fronzen 	= 6
unpaid 		= 8

#score
normal_score= 500
vip_score 	= 1500

#cash_limit
cash_limit 		= [50, 100, 150, 200]

#invalid operation
invalidation = [
	("Delivery Address Must not be left Empty", '/order/comfirm/'), 
	("We have a limit for unpaid order for at most three.", "/"),
	("Sorry, but you have to first recharge your account, or you can choose other pay method.", "/order/comfirm/"),
	("You cannot buy so many by cash, we have a limit for it.", "/current_order/"),
]

paymethods = ["Unipay", "Local Bank", "Cash",]

##################################tools
def newcustomer(owner):
	p = Customer()
	p.level = 0
	p.score = 0
	p.owner = owner

	p.save()
	return p


def imageresize(path):
	im = Image.open(path)

	newsize = im.size
	if newsize[0] < newsize[1]:
		scale = int(newsize[0] / 200.0)
	else:
		scale = int(newsize[1] / 200.0)

	if scale==0:
		return
		
	newsize = [i / scale for i in newsize]

	im = im.resize(newsize, Image.ANTIALIAS)
	
	l = (newsize[0] - 200) / 2
	r = (newsize[1] - 200) / 2
	box = (l, r, l + 200, r + 200)
	im = im.crop(box)
	im.save(path)


def update_book(order):
#	for item in order.orderitem_set.all():
#		Menu.objects.filter(pk=item.menu.id).update(book=F('book')+item.amount)

	for item in order.orderitem_set.all():
		item.menu.book += item.amount
		item.menu.save()

def calc_order(order):
	items = order.orderitem_set.all()
	total = 0.0
	for item in items:	
		total += item.menu.cost * item.amount
	return total

def scores_update(user, total):
	Customer.objects.filter(owner=user).update(score=total)
	if total > normal_score:
		Customer.objects.filter(owner=user).update(level=1)
	elif total > vip_score:
		Customer.objects.filter(owner=user).update(level=2)


####################################views functions

def index(request):
	specs = FoodSpec.objects.all()
	orders = []
	for spec in specs:
		order = spec.menu_set.all()[:10]
		orders.append((spec, order))

	return render(request,'index3.html', {'orders': orders});

def index2(request):
	order = Menu.objects.all()

	order1 = order[:4]
	order2 = order[4:8]
	order3 = order[8:12]

	
	return render(request,'index_cand.html', {'order1':order1, 'order2':order2, 'order3':order3});


def errors_report(request, inval):
	print len(invalidation)
	inval = int(inval)
	if inval >= len(invalidation):
		raise Http404
	return rento('errors_report.html', {'error':invalidation[inval]})
	

@login_required
def personal_info(request):
	user = request.user

	try:
		p = user.customer
	except Customer.DoesNotExist:
		p = newcustomer(user)
#
	if request.method == 'GET':
		form = CustomerForm(instance = p)

	elif request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance = p)
		if form.is_valid():
			user.message_set.create(message='You profile have changed')
			form.save()
			if request.FILES:
				try:
					tmp=form.cleaned_data['image'].__dict__['_name']
					exist=True
				except KeyError:
					exist=False
				if exist:
					path = '/root/web/work/media/'+ unicode(user.customer.image)
					imageresize(str(path))
			return HttpResponseRedirect('/editprofile/')

		##REVICE: should be reviced when homepage is done
	return render(request, 'profile_edit.html', {'form': form, })

@login_required
def local_bank(request):
	user = request.user

#bugs possible
	try:
		account = Account.objects.get(user=user)
	except Account.DoesNotExist:
		account = Account()
		account.money = 0
		user.account = account

	form = AccountForm()
	return render(request, 'local_bank.html', {'form':form, 'money':account.money})

@login_required
def order_history(request, page='1'):
	user = request.user
	try:
		page = int(page)
	except ValueError:
		raise Http404

	page = page-1;
	try:
		orders = user.order_set.order_by("-time").exclude(state = unfinished)
		cnt = orders.count()
		pages = range(1, (cnt+19)/10)

		if page*10 > cnt or page < 0:
			raise Http404
		else:
			orders = orders[page*10:page*10+10]

		cost = []
		for order in orders:
			a = 0
			for item in order.orderitem_set.all():
				a += item.amount * item.menu.cost
			cost.append(a)
		orders = zip(orders, cost)
	except Order.DoesNotExist:
		orders = []
	form = DateForm()
	return render(request, 'order_history.html', {'orders': orders, 'form':form, 'page':page+1, 'pages': pages})



@login_required	
def recommands(request, ajax=False):
	user = request.user

	foods = Menu.objects.order_by('-book')
	recuser = User.objects.get(username = "recommand")

	recorders = Order.objects.filter(user=recuser)

	foods = foods[:6]

	if request.method == 'GET':
		tastes = Taste.objects.all()

		#count.index[count.max()]
		return render(request, 'recommands.html',{'foods':foods, 'recorders':recorders})

	elif request.method == 'POST':
		amount = request.POST.get('amount', '0')
		menuid = request.POST['foodid']
		errors = []
		try:
			amount = int(amount)
			menu = Menu.objects.get(id=menuid)
		except KeyError:
			errors.append('You should fill in a number')

		if amount == 0:
			errors.append('You didn\t add any food, actualy.')
		elif amount < 0:
			errors.append('Well, negative is negative.')

		user = request.user
		try:
			menu = Menu.objects.get(id = menuid)
		except Menu.DoesNotExist:
			errors.append('Invalid POST')

		if errors:
			if ajax:
				return httpr('1')

			for error in errors:
				user.message_set.create(message=error)

			return render(request, 'recommands.html',{'foods':foods, 'recorders':recorders})

		try:
			order = user.order_set.get(state = unfinished)
		except Order.DoesNotExist:
			order = Order()
			order.state = unfinished
			order.user = user
			order.addr = ''
			order.tel = ''
			order.delivery = Delivery.objects.all()[0]
			order.save()

		try:
			orderitem = OrderItem.objects.get(menu=menu, order=order)
			orderitem.amount += amount
		except OrderItem.DoesNotExist:
			orderitem = OrderItem()
			orderitem.order = order
			orderitem.amount = amount
			orderitem.menu = Menu.objects.get(id=menuid)

		orderitem.save()

		if ajax:
			return httpr('0')

		user.message_set.create(message='The food has been added to your order Successfully')		

		return render(request, 'recommands.html',{'foods':foods, 'recorders':recorders})

		
@login_required
def current_order(request):
	user = request.user

	error = 'You have not order any food yet.'
	total = 0.0
	if request.method == "GET":
		try:
			order = user.order_set.get(state=unfinished)
			items = order.orderitem_set.all()
			for item in items:
				total += item.menu.cost * item.amount
			error = ''
		except Order.DoesNotExist:
			items = []
		
	elif request.method == "POST":
		order = get_object_or_404(Order, user=user, state=unfinished)
		order.delete()
		items = []
		error = "Your order has been deleted."
	
	return render(request, 'current_order.html', {'error':error, 'order':items, 'total':total})

@login_required	
def order_update(request, id):

	if request.method == 'POST':
		return httpr('fuck you')

	elif request.method == 'GET':
		user = request.user
		amount = request.GET.get('amount', '0')
		#keyError
		try:
			amount = int(amount)
		except ValueError:
			return httpr('fuck you')
		if (amount < 0):
			return httpr('We cannot support such operaton for a while')

		try:
			menu = Menu.objects.get(id=id)
			order = user.order_set.get(state=unfinished)
			item = order.orderitem_set.get(menu=menu);
		except (Menu.DoesNotExist, Order.DoesNotExist, OrderItem.DoesNotExist):
			return httpr('shit')
	
		if amount > 0:
			item.amount = amount
			item.save()
		else:
			item.delete()
			if not order.orderitem_set.all():
				order.delete()

		return httpr('0')



@login_required
def order_comfirm(request):
	
	user = request.user
	if request.method == "GET":
		order = get_object_or_404(Order, user=user, state=unfinished)
		try:
			customer = user.customer
		except Customer.DoesNotExist:
			customer = newcustomer(user)

		orderitem = order.orderitem_set.all()

		total = 0
		for item in orderitem:
			total += item.menu.cost * item.amount
		
		addrs = user.address_set.all()
		options = paymethods[:customer.level+2]
		
		try:
			account = Account.objects.get(user = user)
			#bugs for not only one account
		except Account.DoesNotExist:
			account = Account()
			account.money = 0
			account.user = user
			account.save()

		money = account.money;

		return render(request, "pay.html", locals())
	else:
		raise Http404


@login_required
def order_committing(request):
	user = request.user
	#update customer_info
	if request.method == "GET":
		print "get"
		raise Http404

	elif request.method == "POST":
		#validate		
		try:
			address = request.POST.get('addr')
			tel = request.POST.get('tel')
			name = request.POST.get('name')
		except KeyError:
			print "keyerror"
			return HttpResponseRedirect("/errors_report/0/")

			return HttpResponseRedirect("/order/comfirm/")

		customer = get_object_or_404(Customer, owner=request.user)
		paymethod = request.POST.get("paymethod", "xxx")
		options = paymethods[:customer.level+2]
		try:
			paymethod = options.index(paymethod)
		except ValueError:
			print "paymethod"
			raise Http404

		order = get_object_or_404(Order, user=user, state=unfinished)
		order.extra_info=request.POST.get("extra-info", "")
		total = calc_order(order)

		#*check for unpaid order, 
		#in case someone keep order by cash but do not pay
		print user.username
		tmp = Order.objects.filter(user=user, state=unpaid).count()
		if tmp > 3:
			#wrong code 2
			return HttpResponseRedirect("/errors_report/1/")
			

#UNIPAY
		if paymethod == 0: 
			return httpr("Sorry, the function haven\' been accomplished yet.")
			return HttpResponseRedirect("/pay/unipay/")

#LOCAL ACCOUNT
		elif paymethod == 1: 
			try:
				account = Account.objects.get(user = user)
				#bugs for not only one account
			except Account.DoesNotExist:
				account = Account()
				account.money = 0
				account.user = user
				account.save()

			account.money -= total 
			if customer.level >= 2:
				overdraft = int((vip_score - customer.score) / 10) - 300
			else:
				overdraft = 0
			if (account.money < overdraft):
				#wrong code 3
				return HttpResponseRedirect("/errors_report/2/")
			else:
				Account.objects.filter(pk = account.id).update(money = F('money')-total)
				order.state = paid
				order.time = datetime.datetime.now()
				
				order.save()
				update_book(order)
				user.message_set.create(message="Paid successfully.<br />We will inform you when the food is done.")
				scores_update(user, total + customer.score)

				return HttpResponseRedirect("/")
			
#CASH
		elif paymethod == 2: #cash
			if total > cash_limit[customer.level]:
				#wrong code 4
				return HttpResponseRedirect("/errors_report/3/")
			order.state = unpaid
			order.time = datetime.datetime.now()
			order.save()
			update_book(order)
			user.message_set.create(message="Order Successfully.")
			return HttpResponseRedirect("/")

@login_required
def order_dup(request, id):
	try:
		id = int(id)
	except ValueError:
		print "here"
		raise Http404


	user = request.user
	old_order = get_object_or_404(Order, id=id)
	

	try:
		cur_order = user.order_set.get(state = unfinished)
	except Order.DoesNotExist:
		cur_order = Order()
		cur_order.state = unfinished
		cur_order.addr = ''
		cur_order.tel = ''
		cur_order.delivery = Delivery.objects.all()[0]
		cur_order.user = user
		cur_order.save()
		

	for item in old_order.orderitem_set.all():
		menu = item.menu
		amount = item.amount

		try:
			orderitem = cur_order.orderitem_set.get(menu = menu)
		except OrderItem.DoesNotExist:
			orderitem = OrderItem()
			orderitem.menu = menu
			orderitem.amount = 0
			orderitem.order = cur_order
		
		orderitem.amount += amount
		orderitem.save()

	return httpr('0')


def foodspec(request, id, page=0):

	spec = get_object_or_404(FoodSpec, id=id)
	order = Menu.objects.filter(foodspec=spec)

	return render(request, 'foodspec.html', {'order': order, 'spec':spec.name})
	


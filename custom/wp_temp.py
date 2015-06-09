

@login_required
def order_committing(request):
	user = request.user
	#update customer_info
	if request.method == "GET":
		raise Http_404

	elif request.method == "POST":
		#validate		
		try:
			address = request.POST.get('addr')
			tel = request.POST.get('tel')
			name = request.POST.get('name')
		except KeyError:
			user.message_set.create(message="Delivery Address Must not be left Empty")
			return HttpResponseRedirect("/pay/")

		customer = get_object_or_404(Customer, owner=request.user)
		paymethod = request.POST.get("paymethod", "xxx")
		options = paymethods[:customer.level+2]
		try:
			paymethod = paymethods.index(options)
		except ValueError:
			raise Http_404

		order = get_object_or_404(Order, user=user, state=unfinished)

		if paymethod == 0: #unipay
			return HttpResponseRedirect("/pay/unipay/")
		elif paymethod == 1: #local account
			total = calc(total)
			try:
				account = user.account
			except AccountDoesNotExist:
				account = Account()
				account.money = 0
				account.user = user
				account.save()

			account.money -= total 
			if (account.money < 0):
				user.message_set.create(message="Sorry, you don't have enough money left, or you can choose other pay method.")
				return HttpResponseRedirect("/order/confirm/")
			else:
				Account.objects.filter(pk = account.id).update(money = F('money')-total)
				order.state = paid
				order.extra_info= request.POST.get("extra-info", "")
				order.save()
				user.message_set.create(message="Paid successfully.")
				user.message_set.create(message="We will inform you foods are done")
				return HttpResponseRedirect("/")
			
		elif paymethod == 2: #cash
			pass
		elif paymethod == 3: #overdraft
			pass
			# revise it, maybe change the db
			order.state = committed
			return httpr("Thank you for your ordering")



#coding=utf-8

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
			user.message_set.create(message="送餐地址不能为空")
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
				user.message_set.create(message="抱歉，账户余额不足，您可以选择其他支付方式")
				return HttpResponseRedirect("/order/confirm/")
			else:
				Account.objects.filter(pk = account.id).update(money = F('money')-total)
				order.state = paid
				order.extra_info= request.POST.get("extra-info", "")
				order.save()
				user.message_set.create(message="支付成功")
				user.message_set.create(message="我们将及时通知您食品是否做好")
				return HttpResponseRedirect("/")
			
		elif paymethod == 2: #cash
			pass
		elif paymethod == 3: #overdraft
			pass
			# revise it, maybe change the db
			order.state = committed
			return httpr("Thank you for your ordering")




	if request.method == 'GET':
		tastes = Taste.object.all()

		
			
		return render(request, 'recommands.html',{'foods':foods})

		
		items = OrderItem.objects.filter(user=user)
		for taste in tastes:
			tmp = items.menu.filter(taste = taste)
			count.append(tmp.aggregate(Sum('amount')

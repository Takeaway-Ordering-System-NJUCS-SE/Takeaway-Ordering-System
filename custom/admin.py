from django.contrib import admin
from work.custom.models import *

class Custadmin(admin.ModelAdmin):
    list_display = ('owner', 'id', 'level', 'score')
    search_display = ('owner', 'id')

class Menuadmin(admin.ModelAdmin):
	list_display = ('name', 'id', 'cost', 'book', 'click', 'description')
	search_display = ('name', 'id')

class orderadmin(admin.ModelAdmin):
	list_display = ('order', 'menu', 'amount')
	
class Msgadmin(admin.ModelAdmin):
	list_display = ('sender', 'receiver', 'title')
	
admin.site.register(Customer, Custadmin)
admin.site.register(Address)
admin.site.register(Delivery)

admin.site.register(Menu, Menuadmin)
admin.site.register(Order)
admin.site.register(OrderItem,orderadmin)
admin.site.register(Message,Msgadmin)
admin.site.register(Account)
admin.site.register(FoodSpec)
admin.site.register(Taste)

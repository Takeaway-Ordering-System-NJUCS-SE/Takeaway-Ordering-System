from django.contrib import admin
from work.custom.models import *

class custadmin(admin.ModelAdmin):
    list_display = ('owner', 'id', 'level', 'score')
    search_display = ('owner', 'id')

class menuadmin(admin.ModelAdmin):
	list_display = ('name', 'id', 'cost', 'book', 'click', 'description')
	search_display = ('name', 'id')



admin.site.register(Customer, custadmin)
admin.site.register(Address)
admin.site.register(Delivery)

admin.site.register(Menu, menuadmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Message)
admin.site.register(Account)
admin.site.register(FoodSpec)
admin.site.register(Taste)

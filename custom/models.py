from django.db import models
from django.contrib.auth.models import User
from PIL import Image

gender_choices = ((u'male', u'Male'), (u'female', u'Female'))

    
class Customer(models.Model):
    owner = models.OneToOneField(User)
    name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length = 6, choices=gender_choices, null=True, blank=True)
    tel = models.CharField(max_length=30, null=True, blank=True)
    level = models.IntegerField()
    score = models.IntegerField()
    image = models.ImageField(upload_to='./profile', null=True, blank=True,)
    #
    def __unicode__(self):
        return unicode(self.name)
    
class FoodSpec(models.Model):
	name = models.CharField(max_length=30)
	def __unicode__(self):
		return unicode(self.name)

class Taste(models.Model):
	name = models.CharField(max_length=30)
	def __unicode__(self):
		return unicode(self.name)


class Menu(models.Model):
    name = models.CharField(max_length=255)
    foodspec = models.ForeignKey(FoodSpec, null=True, blank=True)
    taste = models.ManyToManyField(Taste, null=True, blank=True)
    cost = models.FloatField()
    book = models.IntegerField()
    click = models.IntegerField()
    image = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __unicode__(self):
           return self.name

    
class Address(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    addr = models.CharField(max_length=255)
    tel = models.CharField(max_length=30, null=True, blank=True)
    def __unicode__(self):
        return 'Address' + unicode(self.id) + ': ' + self.addr
    
class Delivery(models.Model):
    name = models.CharField(max_length=30)
    performance = models.IntegerField()
    def __unicode__(self):
        return self.name

class Order(models.Model):
    time = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User)
    addr = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    extra_info = models.CharField(max_length=255, null = True, blank = True)
    delivery = models.ForeignKey(Delivery, null=True)
    state = models.IntegerField()
    menu = models.ManyToManyField(Menu, through='OrderItem')
    def __unicode__(self):
        return 'Order' + unicode(self.id)


   
class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    menu = models.ForeignKey(Menu)
    amount = models.IntegerField()
    def __unicode__(self):
		return 'OrderItem'+unicode(self.id)+' by ' + unicode(self.order)
    
class Message(models.Model):
	type=models.IntegerField()
	user=models.ForeignKey(User, related_name='aaa')
	sender=models.ForeignKey(User,related_name='send_box')
	receiver=models.ForeignKey(User,null=True,blank=True,related_name='receive_box')
	state=models.IntegerField()
	date=models.DateTimeField(auto_now_add=True)
	title=models.CharField(max_length=255,null=True,blank=True)
	content=models.TextField(null=True,blank=True)

	def __unicode__(self):
		return 'Message:'+unicode(self.title)+' sender:'+unicode(self.sender)

class Account(models.Model):
	money = models.FloatField()
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.user.username


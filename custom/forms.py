#coding=utf-8

from django import forms
from custom.models import *
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets
import datetime

genderchoice = (('male', '男'), ('female','女'),)
image_type = ['jpg', 'jpeg', 'png', 'gif', 'tiff', ]

class AddressForm(forms.ModelForm):
	addr=forms.CharField(widget=forms.TextInput(attrs={'size':60}),label='地址')
	def clean_tel(self):
		print 'clean'
		tel=self.cleaned_data['tel']

		result=re.match(r'^[+]?\d*-?\d*$',tel)
		if not result:
			raise forms.ValidationError('无效的电话号码')

		return tel

	class Meta:
		model=Address
		fields=('tel','name','addr')
		#widgets={ 'addr': forms.TextInput(attrs={'size':60},label='地址')}

class ReceiverField(forms.Field):
	def validate(self,value):
		if User.objects.filter(username=value).count()==0:
			raise forms.ValidationError('无效的订单接收者')

class MessageForm(forms.ModelForm):
	dst = ReceiverField(label='收件人')
	
	class Meta:
		model=Message
		fields=('dst','title','content')

	def validate(self,value):
		print value
		super(MessageForm,self).validate(value)

class AccountForm(forms.ModelForm):
	def clean_money(self):
		money = self.cleaned_data['money']
		if money < 0:
			raise forms.ValidationError('无效的金额')
		return money
	class Meta:
		model=Account
		fields=('money',)
    
class DeliveryForm(forms.Form):
    name = forms.CharField(max_length=30)


class DateForm(forms.Form):
	start = forms.DateField(initial=datetime.date.today, widget=widgets.AdminDateWidget())


class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ('name', 'gender', 'tel', 'image')
	
	def clean_image(self):
		image = self.cleaned_data['image']

		
		if not image:
			return image
		
		try:
			s = image.__dict__['_name']
			s = s.split('.')
			s = s[-1]
			s = s.lower()
			if not s in image_type:
				raise forms.ValidationError('不是一个有效的图片文件')
			image.__dict__['_name'] = str(self.instance.owner.username)+'_pic.'+s
		except KeyError:
			pass

		
		return image
#    name = forms.CharField(max_length=50, required=False)
#    gender = forms.ChoiceField(widget=forms.Select, choices=genderchoice, required=False)
#    tel = forms.CharField(max_length=30, required=False)
#    email = forms.EmailField(required=False)
#    image = forms.CharField(max_length=255, required=False)

#class MenuForm(forms.Form):
#    name = forms.CharField(max_length = 255)
#    cost = forms.CharField()
#    #image = forms.CharField(max_length = 255)
#    description = forms.CharField(widget=forms.Textarea, required=False)

class MenuForm(forms.ModelForm):
	class Meta:
		model = Menu
		fields = ('name', 'cost', 'description',)
    
import re




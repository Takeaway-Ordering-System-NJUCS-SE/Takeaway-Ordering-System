from django import forms
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
	required_css_class='required'

from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
	def clean_email(self):
		data=self.cleaned_data['email']
		set=User.objects.filter(email=data)

		if set.count()>0 and self.instance!=set[0]:
			raise forms.ValidationError("This e-mail have been used by others")
		return data
	class Meta:
		model=User
		fields=('email',)

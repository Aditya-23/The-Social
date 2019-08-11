from django import forms
from .models import user, Question


class userregistration(forms.Form):
	username = forms.CharField(required = True, max_length = 20)
	password = forms.CharField(required = True, max_length = 20, min_length = 8)
	firstname = forms.CharField(required = True, max_length = 20)
	lastname = forms.CharField(required = True, max_length = 20)
	email = forms.EmailField(required = True, max_length = 60)

	def __init__(self, *args, **kwargs):
		super(userregistration, self).__init__(*args, **kwargs)


	def clean_password(self):
		password = self.cleaned_data.get('password')
		length = len(password)
		if length < 8 and length > 20:
			raise forms.ValidationError('The password length must be in between 8 and 20')
		special_charracters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_']
		special_character_found = False
		for character in special_charracters:
			if character in password:
				special_character_found = True
				break

		digit_found = False
		lower_found = False
		upper_found = False
		for character in password:
			if character.isupper():
				upper_found = True
			elif character.islower():
				lower_found = True
			if character.isdigit():
				digit_found = True	

		print(special_character_found, upper_found, lower_found, digit_found)
		if not special_character_found or not upper_found or not lower_found or not digit_found:
			raise forms.ValidationError('The password must contain atleast one uppercase, one lowercase character and one digit')
		return password

	
	def save(self, commit = True):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		firstname = self.cleaned_data.get('firstname')
		lastname = self.cleaned_data.get('lastname')
		email = self.cleaned_data.get('email')

		if commit:
			user.objects.create(
			username = username,
			password = password,
			firstname = firstname,
			lastname = lastname,
			email = email
			)



class userlogin(forms.ModelForm):
	class Meta:
		model = user
		fields = [
			'username',
			'password',
		]

class AskQuestion(forms.Form):
	question = forms.CharField(required = True, max_length = 60)
	asked_user = forms.CharField(required = True)

class Answer_form(forms.Form):
	answer = forms.CharField(required = True, max_length = 1000)
	answered_user = forms.CharField(required = True, max_length = 60)

	

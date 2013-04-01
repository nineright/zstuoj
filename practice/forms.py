from django import forms
from zstuoj.practice.models import Users
from zstuoj.practice.utils import *
import re

class LoginForm(forms.Form):
	username = forms.CharField(max_length=20, initial="")
	password = forms.CharField(max_length=32)
	referrer = forms.CharField(widget=forms.HiddenInput)
	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.match('[0-9a-zA-Z_]*', username):
			raise forms.ValidationError('The username should only \
			contain digits alphabets and underscore')
		return username


class RegisterForm(forms.Form):
	user_id = forms.CharField(max_length=20, min_length=3, initial="")
	nick = forms.CharField(max_length=100, initial="")
	email = forms.EmailField(initial="")
	school = forms.CharField(max_length=100, initial="")
	password = forms.CharField(max_length=32)
	re_password = forms.CharField(max_length=32)

	def clean_user_id(self):
		uid = self.cleaned_data['user_id']
		if not re.match('[0-9a-zA-Z_]*', uid):
			raise forms.ValidationError('The username should only \
			contain digits alphabets and underscore')
		if Users.objects.filter(user_id=uid).exists():
			raise forms.ValidationError('The usr_id name has been registered!')
		return uid

	def clean_re_password(self):
		cd = self.cleaned_data
		pw1 = self.cleaned_data['re_password']
		pw2 = self.cleaned_data.get('password')
		if not pw2 or pw1 != pw2:
			raise forms.ValidationError('The two passwords are not same')
		return pw1


class StatusSearchForm(forms.Form):
	uid = forms.CharField(max_length=20, min_length=3,
			initial="", required=False)
	pid = forms.IntegerField(required=False)
	lang = forms.IntegerField(required=False, initial=-1)
	result = forms.IntegerField(required=False, initial=-1)
	top = forms.IntegerField(required=False)

	def clean(self):
		cd = self.cleaned_data
		if cd['uid'] == None:
			cd['uid'] = u""
		if cd['pid'] == None:
			cd['pid'] = u""
		if cd['lang'] == None:
			cd['lang'] = -1
		if cd['result'] == None:
			cd['result'] = -1
		if cd['top'] == None:
			cd['top'] = u""
		return cd


class SubmitForm(forms.Form):
	pid = forms.IntegerField()
	lang = forms.IntegerField()
	source = forms.CharField(widget=forms.Textarea, max_length=65536, min_length=10)



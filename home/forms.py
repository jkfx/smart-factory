from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm

class UserForm(UserChangeForm):
	class Meta:
		model=User
		fields=['email','first_name','last_name']
		labels={
		   'last_name':'手机号码',
		   'first_name':'组织名称'
		}
		widgets={
		'email':forms.TextInput(attrs={'class':'form-control',}),
		'first_name':forms.TextInput(attrs={'class':'form-control',}),
		'last_name':forms.TextInput(attrs={'class':'form-control'}),
		}

class PasswordForm(PasswordChangeForm):
	class Meta:
		model=User
		fields=['old_password','new_password','new_password_confirmation']
		labels={
		   'old_password':'旧密码',
		   'new_password':'新密码',
		   'new_password_confirmation':'确认新密码'
		}
		
		widgets={
		'old_password':forms.TextInput(attrs={'class':'form-control','placeholder':'输入旧密码'}),
		'new_password':forms.TextInput(attrs={'class':'form-control','placeholder':'输入新密码'}),
		'new_password_confirmation':forms.TextInput(attrs={'class':'form-control','placeholder':'再次输入新密码'})
		}


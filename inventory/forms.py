from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import *

TOTAL_FORM_COUNT = 'TOTAL_FORMS'
INITIAL_FORM_COUNT = 'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = 'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = 'MAX_NUM_FORMS'
ORDERING_FIELD_NAME = 'ORDER'
DELETION_FIELD_NAME = 'DELETE'

# default minimum number of forms in a formset
DEFAULT_MIN_NUM = 0

# default maximum number of forms in a formset, to prevent memory exhaustion
DEFAULT_MAX_NUM = 1000
class DateInput(forms.DateInput):
	input_type='date'

class EmployeeForm(forms.ModelForm):
	def __init__(self,data=None,files=None,request=None,recipient_list=None,*args,**kwargs):
		super().__init__(data=data,files=files,*args,**kwargs)
		self.fields['name'].widget.attrs['placeholder']='输入姓名'
		self.fields['address'].widget.attrs['placeholder']='输入地址'
		self.fields['phone'].widget.attrs['placeholder']='输入手机号码'
		self.fields['gender'].widget.attrs['placeholder']='select '

		
	class Meta:
		model=Employee
		fields=('name','designation','address','phone','dob','doj','basicSalary','gender', 'lastSalary', 'bonus', )
		widgets={
		     'dob':DateInput(),
		     'doj':DateInput(),
		     'lastSalary':DateInput(),
		   
		     
		}

class CustomerForm(forms.ModelForm):
	class Meta:
		model=Customer
		fields=('name','address','phone')
		widgets={
		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'输入姓名'}),
		'address':forms.TextInput(attrs={'class':'form-control','placeholder':'输入地址'}),
		'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'输入手机号码'}),

		}		

class WorkForm(forms.ModelForm):
	#emp = forms.IntegerField(widget=forms.HiddenInput())
	product = forms.ModelChoiceField(queryset=Products.objects.all(),  empty_label="选择产品", required=True, label="产品")
	material = forms.ModelChoiceField(queryset=raw_materials.objects.all(),  empty_label="选择原材料", required=True, label="原材料")
	weight  = forms.DecimalField(max_digits=10, decimal_places=2 ,required=True, 
		widget = forms.NumberInput(attrs={ 'step': 0.50,'placeholder': '输入数量（单位：千克）'}),
		label = '数量'
		)
	class Meta:
		model=Work
		#fields=('product', 'weight')
		exclude= ["emp"]

class ProductForm(forms.ModelForm):
	class Meta:
		model=Products
		fields=('name','cost','wages','weight')
		widgets={
		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'输入产品名称'}),
		'cost':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'输入每千克的成本'}),
		'wages':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'输入每千克的报酬'}),
		'weight':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'输入重量（单位：千克）'}),
		}

class OrderForm(forms.ModelForm): 
	class Meta:
		model=Orders
		fields=('cus',)

class OrderNowForm(forms.Form):
	product = forms.ModelChoiceField(queryset=Products.objects.all(),  empty_label="选择产品", required=True, label="产品")
	weight  = forms.DecimalField(max_digits=10, decimal_places=2 ,required=True, 
		widget = forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder': '输入数量（单位：千克）'}),
		label = '数量'
		)

OrderFormset = formset_factory(OrderNowForm, extra=1)


# class OrderNowForm(forms.ModelForm):
# 	class Meta:
# 		model 	= OrderItems
# 		fields 	= ('product', 'weight', )
# 		labels 	= 	{
#             			'product': 'Choose the Product', 
#             			'weight' : 'Quantity (in kg)' 
#         		  	}

# 		widgets =  {
#             			#'product': forms.ModelChoiceField(attrs={ 'class': 'form-control','placeholder': 'Select Product'}), 
#             			'weight' : forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder': 'Enter Quantity'})
#          			}


# OrderModelFormset = modelformset_factory(
#     OrderItems,
#     fields=('product', 'weight', ),
#     extra=1,
# 	widgets = 	{
#         			'weight'  : forms.NumberInput(attrs={ 'step': 0.50, 'class': 'form-control','placeholder': 'Enter Quantity'})
#          		}
# )




	#def __init__(self,data=None,files=None,request=None,recipient_list=None,*args,**kwargs):
	#	super().__init__(data=data,files=files,*args,**kwargs)
	#	self.fields['name'].widget.attrs['placeholder']='name'
	#	self.fields['address'].widget.attrs['placeholder']='address'
	#	self.fields['phone'].widget.attrs['placeholder']='phone'

 
# class SupplierForm(forms.ModelForm):	
#  	class Meta:
#  		model=Supplier
#  		fields=('name','address','phone',)
#  		widgets={
#  		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the  name'}),
# 		'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the addres'}),
# 		'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the phone no'}),

# 		}
	
		
		

class SupplierForm(forms.ModelForm):	
	class Meta:
		model=Supplier
		fields=('name','address','phone',)
		widgets={
		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'输入供应商名称'}),
		'address':forms.TextInput(attrs={'class':'form-control','placeholder':'输入地址'}),
		'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'输入电话号码'}),

		}
       		

class MaterialsForm(forms.ModelForm):
	class Meta:
		model  = raw_materials
		fields = '__all__'
		labels={
		'name':'原材料名称',
		'cost':'材料成本',
		'weight':'可用数额',
		'make':'产品制造百分比',
		}
		widgets={
		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'输入原材料名称'}),
		'cost':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'输入成本'}),
		'weight':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'输入可用数额'}),
		'make':forms.NumberInput(attrs={'step':0.50,'class':'form-control','placeholder':'输入产品制造百分比'}),


		}

	def __init__(self, *args, **kwargs):
		super(MaterialsForm, self).__init__(*args, **kwargs)
		for key in self.fields:
			self.fields[key].required = True

class MaterialsOrderForm(forms.ModelForm):
	sup = forms.ModelChoiceField(queryset=Supplier.objects.all(),  empty_label="选择供应商", required=True,label='供应商')
	material = forms.ModelChoiceField(queryset=raw_materials.objects.all(),  empty_label="选择原材料", required=True, label="原材料")
	weight  = forms.DecimalField(max_digits=10, decimal_places=2 ,required=True, 
	 	widget = forms.NumberInput(attrs={ 'step': 0.50,'placeholder': '输入数量（单位：千克）'}),
	 	label = '数量'
	 	)
	class Meta:
		model  = materials_order
		fields = ('sup', 'material', 'weight')


class AccountForm(forms.ModelForm):
	money = forms.DecimalField(
		max_digits=15, decimal_places=2 ,required=True, 
		widget = forms.NumberInput(attrs={ 'step': 50.00,'class':'form-control','placeholder': '输入初始账户余额'}),
		label = "公司初始金额" 
	)
	class Meta:
		model  = Accounts
		fields = ('money',)


class TransactionForm(forms.ModelForm):

	class Meta:
		model  = Transaction
		fields = '__all__'
		widgets={
		  'date':DateInput()
		}
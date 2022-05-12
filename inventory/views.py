from __future__ import unicode_literals
from cv2 import COLOR_RGB2BGR
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.db.models import Q
from .models import *	
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django_tenants.utils import schema_context

# from reportlab.pdfgen import canvas
# from weasyprint import HTML
# from weasyprint.fonts import FontConfiguration
from django.template.loader import render_to_string

import threading
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import pandas as pd
import os
import cv2
from PIL import Image
import datetime
import os
from pathlib import Path

# Create your views here.
def get_profit(tr):
	res = 0 
	for t in tr:
		if t.type == 0 :
			res += t.amt 
	return res 			

def get_expenses(tr):
	res = 0 
	for t in tr:
		if t.type == 1 :
			res += t.amt 
	return res

@login_required(login_url='home:login')
def dashboard(request):
	with schema_context(request.user.username ):
		today 	= datetime.date.today()

		month = []
		for i in range(1, 13):
			tr 	= Transaction.objects.filter(date__month=i, date__year=today.year)	
			pro = get_profit(tr)
			exp = get_expenses(tr)
			month.append(int(pro-exp))

		tr = Transaction.objects.filter(date__month=today.month, date__year=today.year)
		income 	= get_profit(tr)
		expenses = get_expenses(tr)

		try:
			profit_percentage = int(((income-expenses) / expenses ) * 100)
		except ZeroDivisionError:
			profit_percentage = 100 

		dict = { 

			"initial" 	: get_object_or_404(Accounts, name=request.user.username) ,
			"income"   	: income ,
			"expenses"	: expenses ,
			"profit_percentage"	: profit_percentage , 
			"loss_percetage"	: 100 - profit_percentage ,  
		}

		return render(request, 'inventory/dashboard.html', { 'dict' : dict , 'trans' : tr , 'month' : month })



@login_required(login_url='home:login')
def add_amount(request):
	with schema_context(request.user.username ):
		ac = get_object_or_404(Accounts, name=request.user.username)
		if request.method == "POST":
			form = AccountForm(request.POST, instance=ac)
			if form.is_valid():
				form.save()
				messages.success(request, '账户更新')
				return redirect('inventory:dashboard')
			else:
				messages.error(request, '账户未更新')
				messages.error(request, form.errors)
		else:
			form = AccountForm(instance=ac)
		header = "初始账户余额"
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })


# _____________________ For Transactions _______________________________

@login_required(login_url='home:login')
def view_credit(request):
	with schema_context(request.user.username ):
		tr 	   = Transaction.objects.filter(type=0)
		header = "入账交易详情"
		return render(request, 'inventory/transaction.html', { 'trans' : tr, "header" : header })


@login_required(login_url='home:login')
def view_debit(request):
	with schema_context(request.user.username ):
		tr 	   = Transaction.objects.filter(type=1)
		header = "出账交易详情"
		return render(request, 'inventory/transaction.html', { 'trans' : tr, "header" : header })

@login_required(login_url='home:login')
def view_all_transaction(request):
	with schema_context(request.user.username ):
		tr 	   = Transaction.objects.all()
		header = "所有交易详情"
		return render(request, 'inventory/transaction.html', { 'trans' : tr, "header" : header })

# Have to complete accounts 
@login_required(login_url='home:login')
def add_transaction(request):
	with schema_context(request.user.username ):
		form=TransactionForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=TransactionForm(request.POST)
			if form.is_valid():
				amt  = form.cleaned_data.get('amt')
				type = form.cleaned_data.get('type')
				des  = form.cleaned_data.get('description')
				ac 	 = get_object_or_404(Accounts, name=request.user.username)

				if type == 1 and ac.is_available(amt) == False :
					messages.error(request, '抱歉，账户余额不足')	
					messages.error(request, '{} 薪资未被更新'.format(emp))	
					return redirect('inventory:salary_cal')

				if type == 1 :
					ac.reduce_amt(amt)
				else:
					ac.increase_amt(amt)
				ac.save()

				form.save()
				messages.success(request, des )
				return redirect('inventory:dashboard')
			else:
				messages.error(request, '交易失败。')
				messages.error(request, form.errors)
		header = "新交易记录" 
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


	
# _____________________ For Employee _______________________________

@login_required(login_url='home:login')
def employee(request):
	with schema_context(request.user.username ):
	#with connection.cursor() as cursor:
		#cursor.execute(f"SET search_path to " + )
		Emps = Employee.objects.all()
		return render(request, 'inventory/employee.html', { 'Emps': Emps })   
@login_required(login_url='home:login')
def add_employee(request):
	with schema_context(request.user.username ):
		form=EmployeeForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=EmployeeForm(request.POST)
			if form.is_valid():
				form.save()
				# os.mkdir("inventory/static/facerec/data/infer/"+)
				messages.success(request, '添加员工成功。')
				return redirect('inventory:employee')
			else:
				messages.error(request, '员工未被添加。')
				messages.error(request, form.errors)
		header = "在此创建员工" 
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })

		
@login_required(login_url='home:login')
def emp_edit(request, emp_id):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		if request.method == "POST":
			form = EmployeeForm(request.POST, instance=emp)
			if form.is_valid():
				form.save()
				messages.success(request, '{} 已更新'.format(emp.name))
				return redirect('inventory:employee')
			else:
				messages.error(request, '{} 未被更新'.format(emp.name))
				messages.error(request, form.errors)
		else:
			form = EmployeeForm(instance=emp)
		header = "{} 详情".format(emp)
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })

@login_required(login_url='home:login')
def delete_employee(request, emp_id):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		messages.success(request, '{} 已被删除。'.format(emp))
		emp.delete()
		return redirect('inventory:employee')

@login_required(login_url='home:login')
def view_works(request, emp_id):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		wk = Work.objects.filter(emp=emp_id)
		return render(request, 'inventory/view_works.html', { 'wk' : wk, 'emp' : emp })

@login_required(login_url='home:login')
def add_work(request, emp_id):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		if request.method=="POST":
			form=WorkForm(request.POST)
			if form.is_valid():
				form = form.save(commit=False)
				form.emp = emp 
				if(form.material.is_available(form.weight)):
					form.product.add_product(form.weight)
					form.material.reduce(form.weight)
					try:
						raw_waste = Products.objects.get(name='raw_waste')
					except ObjectDoesNotExist:
						raw_waste = Products(name='raw_waste', cost=0, wages=0, weight=0)

					w = ( form.weight / form.material.getmake()) - form.weight 

					raw_waste.add_product(w)
					raw_waste.save()

					emp.add_bonus(form.product.get_wages() * form.weight)
					emp.save()
					form.save()
					messages.success(request, '{} 工作任务已更新'.format(emp))
					return view_works(request, emp_id)
				else:
					messages.error(request, '没有这么多的原材料来制造这种产品')
			messages.error(request, '{} 工作任务未被更新'.format(emp))

		header = "为 {} 添加工作任务".format(emp)
		form = WorkForm(initial={'emp': emp })
		return render(request, 'inventory/add_common.html', {'form' : form, 'header' : header })


# _____________________ For ProductS _______________________________

@login_required(login_url='home:login')
def product_details(request):
	with schema_context(request.user.username ):
		pro = Products.objects.all()
		return render(request, 'inventory/product_details.html', { 'pro': pro })	

@login_required(login_url='home:login')
def add_product(request):
	with schema_context(request.user.username ):
		form=ProductForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=ProductForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, '产品已被创建')
				return redirect('inventory:product_details')
			else:
				messages.error(request, '产品未被创建')
				messages.error(request, form.errors)
		header = '创建新产品'
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })

@login_required(login_url='home:login')
def edit_product(request, pro_id):
	with schema_context(request.user.username ):
		pro = get_object_or_404(Products, pk=pro_id)
		if request.method == "POST":
			form = ProductForm(request.POST, instance=pro)
			if form.is_valid():
				form.save()
				messages.success(request, '{} 已被更新'.format(pro))
				return redirect('inventory:product_details')
		else:
			form = ProductForm(instance=pro)
		header = "{} 详情".format(pro) 
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })


@login_required(login_url='home:login')
def delete_product(request, pro_id):
	with schema_context(request.user.username ):
		pro = get_object_or_404(Products, pk=pro_id)
		messages.success(request, '{} 已被删除'.format(pro))
		pro.delete()
		return redirect('inventory:product_details')


# _____________________ For Salary _______________________________

@login_required(login_url='home:login')
def get_total(request):
	with schema_context(request.user.username ):
		emp = Employee.objects.all()
		for e in emp :
			e.total = e.bonus + e.basicSalary 
			e.save()

@login_required(login_url='home:login')
def salary_details(request, emp_id): # for single employee 
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		sal = Salary.objects.filter(emp=emp)
		return render(request, 'inventory/salary_details.html', {'sal': sal, 'emp' : emp } )


@login_required(login_url='home:login')
def pay_now(request, emp_id, isall=False):
	with schema_context(request.user.username ):
		emp = get_object_or_404(Employee, pk=emp_id)
		ac = get_object_or_404(Accounts, name=request.user.username)

		if ac.is_available(emp.total) == False :
			messages.error(request, '抱歉，账户余额不足')	
			messages.error(request, '{} 薪资未被更新'.format(emp))	
			return redirect('inventory:salary_cal')

		s 	= Salary(emp=emp, basicSalary=emp.basicSalary, bonus=emp.bonus, total=emp.total)
		s.save()
		emp.isPaid 	= True
		emp.bonus 	= 0  
		emp.lastSalary = now()
		emp.save()

		ac.reduce_amt(s.total)

		des = "{} 薪资已支付".format(emp)
		Transaction(amt=s.total, description=des, type=1).save()

		if isall :
			return  
		messages.success(request, '向 {} 支付薪资'.format(emp))	
		return redirect('inventory:salary_cal')


@login_required(login_url='home:login')
def pay_all(request):
	with schema_context(request.user.username ):
		emp = Employee.objects.all()
		ac = get_object_or_404(Accounts, name=request.user.username)
		
		t = 0 
		for e in emp :
			if e.isPaid == 0 :
				t += e.total 

		if ac.is_available(t) == False :
			messages.error(request, '抱歉 (・_・), 账户余额不足')	
			messages.error(request, '薪资未被更新')	
			return redirect('inventory:salary_cal')

		for e in emp :
			if e.isPaid == 0 :
				pay_now(request, e.id, True)
		messages.success(request, '全部支付')
		return redirect('inventory:salary_cal')


@login_required(login_url='home:login')
def salary_cal(request): # salary details for all employee
	with schema_context(request.user.username ):
		get_total(request) 	
		emp = Employee.objects.all()
		for e in emp : 
			if ( now().date() - e.lastSalary > timedelta(days=7) ) :
				e.isPaid = False 
				e.save()
		return render(request, 'inventory/salary_cal.html', {'emp' : emp })


# _____________________ For customer _______________________________

@login_required(login_url='home:login')
def customer(request):
	with schema_context(request.user.username ):
		cus = Customer.objects.all()
		return render(request, 'inventory/customer.html', { 'cus': cus })	

@login_required(login_url='home:login')
def add_customer(request):
	with schema_context(request.user.username ):
		form=CustomerForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=CustomerForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, '客户已创建')
				return redirect('inventory:customer')
			else:
				messages.error(request, '客户未被创建')
				messages.error(request, form.errors)
		header = '创建客户' 
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


@login_required(login_url='home:login')
def cust_edit(request, cus_id):
	with schema_context(request.user.username ):
		cus = get_object_or_404(Customer, pk=cus_id)
		if request.method == "POST":
			form = CustomerForm(request.POST, instance=cus)
			if form.is_valid():
				form.save()
				messages.success(request, '{} 已更新'.format(cus))
				return redirect('inventory:customer')
			else:
				messages.error(request, '客户未被更新')
				messages.error(request, form.errors)
		else:
			form = CustomerForm(instance=cus)
		header = "{} 详情".format(cus)
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })


@login_required(login_url='home:login')
def delete_customer(request, cus_id):
	with schema_context(request.user.username ):
		cus = get_object_or_404(Customer, pk=cus_id)
		messages.success(request, '{} 已被删除'.format(cus))
		cus.delete()
		return redirect('inventory:customer')

# _____________________ For Orders _______________________________
			

@login_required(login_url='home:login')
def order_all(request): # view all orders
	with schema_context(request.user.username ):
		return render(request, 'inventory/order.html', {'order' : Orders.objects.all() })


@login_required(login_url='home:login')
def order_not_delivered(request): # view not delivered orders
	with schema_context(request.user.username ):
		return render(request, 'inventory/order.html', {'order' : Orders.objects.filter(isDelivered=False) })


@login_required(login_url='home:login')
def order_delivered(request): # view delivered orders
	with schema_context(request.user.username ):
		return render(request, 'inventory/order.html', {'order' : Orders.objects.filter(isDelivered=True) })


@login_required(login_url='home:login')
def order_list(request, cus_id): # for particular customer 
	with schema_context(request.user.username ):
		cus = get_object_or_404(Customer, pk=cus_id)
		order = Orders.objects.filter(cus=cus_id)
		return render(request, 'inventory/order.html', {'order' : order})



@login_required(login_url='home:login')
def order_details(request, ord_id): # particular order details 
	with schema_context(request.user.username ):
		order = get_object_or_404(Orders, pk=ord_id)
		items = OrderItems.objects.filter(order=ord_id)
		return render(request, 'inventory/order_details.html', {'items' : items, 'order' : order })	


# def download_order(request, ord_id): # Billing download for 
# 	with schema_context(request.user.username ):
# 		order = get_object_or_404(Orders, pk=ord_id)
# 		items = OrderItems.objects.filter(order=ord_id)

# 		filename = 'Gi_' + str(order.cus.name) + "_" + str(order.id) 
# 		response = HttpResponse(content_type="application/pdf/force-download")
# 		response['Content-Disposition'] = "inline; filename={}.pdf".format(filename)
		
# 		html = render_to_string('inventory/order_details.html', {'items' : items, 'order' : order })
# 		font_config = FontConfiguration()

# 		HTML(string=html).write_pdf(response, font_config=font_config)

# 		return response

@login_required(login_url='home:login')
def order_now(request, cus_id): # for booking order 
	with schema_context(request.user.username ):
		if request.method == 'POST':
			formset = OrderFormset(request.POST)
			if formset.is_valid() :
				cus 	= get_object_or_404(Customer, pk=cus_id)
				total 	= 0 
				order 	= Orders(cus=cus, total_amt=total, Odate=now())
				order.save() 
				for form in formset: 
					if form.cleaned_data.get('product') and form.cleaned_data.get('weight'):
						product = form.cleaned_data.get('product')
						weight 	= form.cleaned_data.get('weight')
						total  += ( product.cost * weight ) 
						items 	= OrderItems(order=order,product=product, weight=weight) 
						items.save()

				if total : 
					order.total_amt = total 
					order.save() 
					messages.success(request, '订单已预订')
					return redirect('inventory:customer')
				else :
					messages.error(request, "订单未预订")

			else:
				for e in formset.errors :
					messages.error(request, e )
		else:
			formset = OrderFormset(request.GET or None)
		return render(request, 'inventory/order_now.html', { 'formset': formset })


@login_required(login_url='home:login')
def delivered(request, ord_id): # completing the order 
	with schema_context(request.user.username ):
		order 			  = get_object_or_404(Orders, pk=ord_id)
		items 			  = OrderItems.objects.filter(order=order)
		for i in items :
			if(i.product.is_available(i.weight) == False):
				messages.error(request, '{} 已经断货!'.format(i.product.name))
				messages.error(request, '订单无法送达')
				return redirect('inventory:order_all')

		for i in items :
			i.product.reduce_product(i.weight)

		ac = get_object_or_404(Accounts, name=request.user.username)
		ac.increase_amt(order.total_amt)
		ac.save()

		des = "订单 {} 已完成".format(order.cus)
		Transaction(amt=order.total_amt, description=des, type=0).save()

		order.Ddate 	  = now()
		order.isDelivered = True
		order.save()
		messages.success(request, '订单已完成.')
		return redirect('inventory:order_all')


# _____________________ For Supplier _______________________________


@login_required(login_url='home:login')
def supplier(request):
	with schema_context(request.user.username ):
		Sup = Supplier.objects.all()
		return render(request, 'inventory/supplier.html', { 'Sup': Sup })


@login_required(login_url='home:login')
def add_supplier(request):
	with schema_context(request.user.username ):
		form=SupplierForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=SupplierForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, '供应商已创建')
				return redirect('inventory:supplier')
				
			else:
				print(form.errors)
				messages.error(request, '供应商未创建')
				messages.error(request, form.errors)
				
		header = '添加供应商'
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


@login_required(login_url='home:login')
def sup_edit(request, sup_id):
	with schema_context(request.user.username ):
		sup = get_object_or_404(Supplier, pk=sup_id)
		form = SupplierForm(instance=sup)
		if request.method == "POST":
			form = SupplierForm(request.POST, instance=sup)
			if form.is_valid():
				form.save()
				messages.success(request, '{} 已修改'.format(sup))
				return redirect('inventory:supplier')
			else:
				messages.error(request, '{} 未修改'.format(sup))
				messages.error(request, form.errors)
		header = "修改 {}".format(sup)
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })	


@login_required(login_url='home:login')
def delete_supplier(request, sup_id):
	with schema_context(request.user.username ):
		sup = get_object_or_404(Supplier, pk=sup_id)
		messages.success(request, '{} 已删除'.format(sup))
		sup.delete()
		return redirect('inventory:supplier')		


@login_required(login_url='home:login')
def buy_material(request):
	with schema_context(request.user.username ):
		form=MaterialsOrderForm(request.POST or None, request.FILES or None)
		if request.method=="POST":
			form=MaterialsOrderForm(request.POST)
			if form.is_valid():
				material = form.cleaned_data.get('material')
				sup 	 = form.cleaned_data.get('sup')
				weight 	 = form.cleaned_data.get('weight')
				rm 		 = get_object_or_404(raw_materials, name=material)
				sup  	 = get_object_or_404(Supplier, name=sup)
				ac 		 = get_object_or_404(Accounts, name=request.user.username)
				if ac.is_available(rm.cost * weight ) == False :
					messages.error(request, '抱歉 (・_・), 账户余额不足')	
					messages.error(request, '{} 未被购买'.format(material))	
					return redirect('inventory:materials')

				ac.reduce_amt(rm.cost * weight)

				des = "{} 购买于 {}".format(material, sup )
				Transaction(amt=rm.cost * weight, description=des, type=1).save()

				rm.update_weight(weight)
				rm.save() 

				materials_order(sup=sup, material=rm, weight=weight, total_amt=rm.cost * weight).save()

				messages.success(request, des)
				return redirect('inventory:view_purchase')
			else:
				messages.error(request, form.errors)
		header = '购买原材料'
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


@login_required(login_url='home:login')
def view_purchase(request):
	with schema_context(request.user.username ):
		mat = materials_order.objects.all()
		return render(request, 'inventory/view_purchase.html', { 'mat': mat })


# _____________________ For Raw Materials _______________________________


@login_required(login_url='home:login')
def materials(request):
	with schema_context(request.user.username ):
		mat = raw_materials.objects.all()
		return render(request, 'inventory/materials.html', { 'mat': mat })


@login_required(login_url='home:login')
def add_material(request):
	with schema_context(request.user.username ):
		form=MaterialsForm()
		if request.method=="POST":
			form=MaterialsForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, '原材料已创建')
				return redirect('inventory:materials')
			else:
				messages.error(request, '原材料未创建')
				messages.error(request,  form.errors)
		header = "添加新的原材料" 
		return render(request,'inventory/add_common.html',{'form': form, 'header' : header })


@login_required(login_url='home:login')
def material_edit(request, mat_id):
	with schema_context(request.user.username ):
		mat = get_object_or_404(raw_materials, pk=mat_id)
		if request.method == "POST":
			form = MaterialsForm(request.POST, instance=mat)
			if form.is_valid():
				form.save()
				messages.success(request, '{} 已更新'.format(mat))
				return redirect('inventory:materials')
			else:
				messages.error(request,  form.errors)
		form 	= MaterialsForm(instance=mat)
		header  = "更新 {}".format(mat)   
		return render(request, 'inventory/add_common.html', {'form': form, 'header' : header })


@login_required(login_url='home:login')
def delete_material(request, mat_id):
	with schema_context(request.user.username ):
		mat = get_object_or_404(raw_materials, pk=mat_id)
		messages.success(request, '{} 已删除'.format(mat))
		mat.delete()
		return redirect('inventory:materials')


def collate_fn(x):
    return x[0]
workers = 0 if os.name == 'nt' else 8
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))
mtcnn = MTCNN()
resnet = torch.load("inventory/static/facerec/model/model.pth", map_location=torch.device('cpu')).eval()
resnet.classify = False
dataset = datasets.ImageFolder('inventory/static/facerec/data/infer')
dataset.idx_to_class = {i:c for c, i in dataset.class_to_idx.items()}
loader = DataLoader(dataset, collate_fn=collate_fn, num_workers=workers)
aligned = []
names = []
for x, y in loader:
	x_aligned, prob = mtcnn(x, return_prob=True)
	if x_aligned is not None:
		aligned.append(x_aligned)
		names.append(dataset.idx_to_class[y])
aligned = torch.stack(aligned).to(device)
embeddings = resnet(aligned).detach().cpu()

@login_required(login_url='home:login')
def facerec(request):
	with schema_context(request.user.username):
		name = ""
		cap = cv2.VideoCapture(0)
		while True:
			ret, img = cap.read()
			if ret:
				img_cropped = mtcnn(img)
				if img_cropped is not None:
					img_embedding = resnet(img_cropped.unsqueeze(0))
					distance = (img_embedding - embeddings).norm(dim=1)
					if distance.min().item() < 1:
						name = names[distance.argmin().item()]
						messages.success(request, '{} 已签到'.format(name))
						break
					else:
						name = ""
				cv2.imshow("Face Recognition", img)
				if ord('q') == cv2.waitKey(1):
					messages.error(request, '人脸签到退出')
					break
		cap.release()
		cv2.destroyAllWindows()
		if name != "":
			emp = get_object_or_404(Employee, name=name)
			dt = datetime.datetime.now()
			signtab = SigninTab(employee=emp, signintime=dt)
			signtab.save()
		return render(request, 'inventory/attendance.html', {"signintab":SigninTab.objects.all()})

@login_required(login_url='home:login')
def attendance(request):
	with schema_context(request.user.username):
		return render(request, 'inventory/attendance.html', {"signintab":SigninTab.objects.all()})
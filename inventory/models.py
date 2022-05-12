import datetime
from django.utils.timezone import now
from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.

# models.DateField(auto_now_add=True) use this 

CREDIT 	= 0 # means incoming
DEBIT 	= 1 # means Outgoing
Transaction_Type = [(CREDIT, 'Credit'), (DEBIT, 'Debit')]

class Accounts(models.Model): # company Account 
	name  = models.CharField("用户名", max_length=30)
	money = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="账户余额")

	def __str__(self):
		return str(self.money)

	def is_available(self, m):
		return (self.money-m >= 0 )

	def reduce_amt(self, m):
		self.money -= m 
		self.save()

	def increase_amt(self, m):
		self.money += m 
		self.save()

class Transaction(models.Model):	
	amt 		= models.DecimalField(max_digits=15, decimal_places=2, verbose_name="交易金额")
	description = models.CharField("交易描述", max_length=200)
	TYPE_CREDIT = 0
	TYPE_DEBIT 	= 1
	TYPE_CHOICES= [(TYPE_CREDIT, '入账'), (TYPE_DEBIT, '出账') ]
	type		= models.BooleanField(choices=TYPE_CHOICES, verbose_name="类型")
	date  		= models.DateField('交易日期',default=datetime.date.today)

	def __str__(self):
		return self.description 


class raw_materials(models.Model): # commpany Stock 
	name 	 = models.CharField("原材料名称", max_length=30)
	cost 	 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="材料成本")
	weight 	 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="目前可用")
	make     = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="产品制造百分比")

	def __str__(self):
		return self.name 

	def getmake(self): # it will return 0-1 value for 0-100 percentage 
		return self.make/100 

	def is_available(self, w): # use before reduce
		if(self.weight >= w/self.getmake()):
			return True 
		return False 

	def reduce(self, w): # use for update work 
		self.weight -= w/self.getmake() 
		self.save() 

	def update_weight(self, weight):
		self.weight += weight 
		self.save()

class Products(models.Model):
	name 	= models.CharField("产品名称", max_length=30)
	cost 	= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="成本") # cost per Kg
	wages 	= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="报酬") # wages per Kg
	weight 	= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="重量") # weight of the products in kg

	def is_available(self, w): # use before reduce_product 
		return ((self.weight - w) >= 0)

	def reduce_product(self, w): # use for customer delivery  
		self.weight -= w
		self.save()

	def add_product(self, w): # Employee add products AND raw waste will add
		self.weight += w
		self.save()

	def get_wages(self):
		return self.wages 

	def __str__(self):
		return self.name 

class Employee(models.Model):
	name 		= models.CharField("员工姓名", max_length=30)

	# Salary info 
	basicSalary = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="基本工资")
	bonus 		= models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="奖金")
	total 		= models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="共计") # basic + bonus
	isPaid 		= models.BooleanField(default=False, verbose_name="是否支付薪资")
	lastSalary 	= models.DateField('最后一次工资更新日期',)

	DESIGNATION_CEO= '经理'
	DESIGNATION_WORKER= '工人'
	DESIGNATION_SUPERVISER= '监事长'
	DESIGNATION_MARKETING= '营销主管'
	DESIGNATION_OTHERS= '其他'
	DESIGNATION_CHOICES= [(DESIGNATION_WORKER, '工人'),(DESIGNATION_CEO,'经理'),(DESIGNATION_SUPERVISER,'监事长'),(DESIGNATION_MARKETING,'营销主管'),(DESIGNATION_OTHERS,'其他') ]
	
	designation = models.CharField(choices=DESIGNATION_CHOICES, max_length=200,default='其他', verbose_name="职称")
	address = models.CharField(max_length=70, verbose_name="地址")
	phone = models.CharField("电话号码", max_length=11)
	dob = models.DateField('出生日期',  )
	doj = models.DateField('入职日期',  )

	GENDER_MALE 	= 0
	GENDER_FEMALE 	= 1
	GENDER_OTHERS 	= 2
	GENDER_CHOICES 	= [(GENDER_MALE, '男性'), (GENDER_FEMALE, '女性'), (GENDER_OTHERS, '其他') ]
	gender 			= models.IntegerField(choices=GENDER_CHOICES,default=2, verbose_name="性别")

	def __str__(self):
		return self.name

	def update_work(self, weight):
		self.product.add_product(weight)
		self.salary.add_amount(weight * product.wage)
		self.save()

	def add_bonus(self, amt):
		self.bonus += amt 
		self.isPaid = 0 
		self.save()

class SigninTab(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="员工")
	signintime = models.DateTimeField("签到时间")
	def __str__(self):
		return self.employee.name + str(self.signintime)

class Salary(models.Model):
	emp 		= models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="员工")
	basicSalary = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="基本工资")
	bonus 		= models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="奖金")
	total 		= models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="共计") # basic + bonus
	paidDate 	= models.DateField('支付日期', default=datetime.date.today)

class Work(models.Model):
	emp 	 = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="员工")
	product  = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="产品")
	material = models.ForeignKey(raw_materials, on_delete=models.CASCADE, verbose_name="原材料")
	weight 	 = models.DecimalField(max_digits=12, decimal_places=2,  default=0.0, verbose_name="重量")

# ____________________ For Customer and Orders models ________________________

class Customer(models.Model):
	name 	= models.CharField("客户姓名", max_length=30 )
	address = models.CharField(max_length=70, verbose_name="地址")
	phone 	= models.CharField("手机号码", max_length=11)

	def __str__(self):
		return self.name ; 


class Orders(models.Model):

	"""
	Contains a list of orders. 
	One row per order. 
	Each order is placed by a customer and has a Customer_ID - which can be used to link back to the customer record.
	
	""" 
	cus 		= models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="客户")
	Odate 		= models.DateField('下单日期', default=datetime.date.today)
	Ddate 		= models.DateField('送达日期',default=datetime.date.today )
	total_amt 	= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总共数量")
	isDelivered = models.BooleanField(default=False, verbose_name="是否送达")

	def __str__(self):
		return "Order of " + self.cus 


class OrderItems(models.Model):

	"""
	Contains a list of order items. 
	One row for each item on an order - so each Order can generate multiple rows in this table. 
	Each item ordered is a product from your inventory, so each row has a product_id, which links to the products table.
	
	"""
	order 		= models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name="订单")
	product 	= models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="产品")
	weight		= models.DecimalField(max_digits=10, decimal_places=2, verbose_name="重量") # weight of the products in kg


# ____________________ For Supplier and Materials models ________________________

class Supplier(models.Model):
	name 	= models.CharField("供应商名称", max_length=30)
	address = models.CharField(verbose_name="地址",max_length=70)
	phone 	= models.CharField("电话号码", max_length=11)

	def __str__(self):
		return self.name ;

class materials_order(models.Model): # for purchasing raw materials                            
	sup 	 = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="供应商")	
	material = models.ForeignKey(raw_materials, on_delete=models.CASCADE, verbose_name="原材料")	
	weight 	 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="重量")	

	total_amt= models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="总共数量")
	date 	 = models.DateField('购买日期', default=datetime.date.today )

	def __str__(self):
		return "{} 购买于 {}".format(self.material, self.sup)



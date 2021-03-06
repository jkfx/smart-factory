# Generated by Django 3.2.12 on 2022-04-11 02:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='money',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='账户余额'),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='name',
            field=models.CharField(max_length=30, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=70, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=30, verbose_name='客户姓名'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address',
            field=models.CharField(max_length=70, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='basicSalary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='基本工资'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='bonus',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='奖金'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='designation',
            field=models.CharField(choices=[('工人', '工人'), ('经理', '经理'), ('监事长', '监事长'), ('营销主管', '营销主管'), ('其他', '其他')], default='Others', max_length=200, verbose_name='职称'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='dob',
            field=models.DateField(verbose_name='出生日期'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='doj',
            field=models.DateField(verbose_name='入职日期'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.IntegerField(choices=[(0, '男性'), (1, '女性'), (2, '其他')], default=2, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='isPaid',
            field=models.BooleanField(default=False, verbose_name='是否支付薪资'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='lastSalary',
            field=models.DateField(verbose_name='最后一次工资更新日期'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=30, verbose_name='员工姓名'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='电话号码'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='共计'),
        ),
        migrations.AlterField(
            model_name='materials_order',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='购买日期'),
        ),
        migrations.AlterField(
            model_name='materials_order',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.raw_materials', verbose_name='原材料'),
        ),
        migrations.AlterField(
            model_name='materials_order',
            name='sup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.supplier', verbose_name='供应商'),
        ),
        migrations.AlterField(
            model_name='materials_order',
            name='total_amt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='总共数量'),
        ),
        migrations.AlterField(
            model_name='materials_order',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='重量'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.orders', verbose_name='订单'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.products', verbose_name='产品'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='重量'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='Ddate',
            field=models.DateField(default=datetime.date.today, verbose_name='送达日期'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='Odate',
            field=models.DateField(default=datetime.date.today, verbose_name='下单日期'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='cus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.customer', verbose_name='客户'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='isDelivered',
            field=models.BooleanField(default=False, verbose_name='是否送达'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='total_amt',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='总共数量'),
        ),
        migrations.AlterField(
            model_name='products',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='成本'),
        ),
        migrations.AlterField(
            model_name='products',
            name='name',
            field=models.CharField(max_length=30, verbose_name='产品名称'),
        ),
        migrations.AlterField(
            model_name='products',
            name='wages',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='报酬'),
        ),
        migrations.AlterField(
            model_name='products',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='重量'),
        ),
        migrations.AlterField(
            model_name='raw_materials',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='材料成本'),
        ),
        migrations.AlterField(
            model_name='raw_materials',
            name='make',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='产品制造百分比'),
        ),
        migrations.AlterField(
            model_name='raw_materials',
            name='name',
            field=models.CharField(max_length=30, verbose_name='原材料名称'),
        ),
        migrations.AlterField(
            model_name='raw_materials',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='目前可用'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='basicSalary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='基本工资'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='bonus',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='奖金'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='emp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.employee', verbose_name='员工'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='paidDate',
            field=models.DateField(default=datetime.date.today, verbose_name='支付日期'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='共计'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.CharField(max_length=70, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=30, verbose_name='供应商名称'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='phone',
            field=models.CharField(max_length=11, verbose_name='电话号码'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amt',
            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name='交易金额'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='交易日期'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.CharField(max_length=200, verbose_name='交易描述'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.BooleanField(choices=[(0, '入账'), (1, '出账')], verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='work',
            name='emp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.employee', verbose_name='员工'),
        ),
        migrations.AlterField(
            model_name='work',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.raw_materials', verbose_name='原材料'),
        ),
        migrations.AlterField(
            model_name='work',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.products', verbose_name='产品'),
        ),
        migrations.AlterField(
            model_name='work',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='重量'),
        ),
    ]

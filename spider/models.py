from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    name = models.CharField('姓名', max_length=64)
    age = models.SmallIntegerField('年龄')
    choices = (
        (1, '男'),
        (2, '女'),
        (3, '未知')
    )
    sex = models.SmallIntegerField('性别', choices=choices)

class OrderCrawl(models.Model):
    asin = models.CharField(max_length=255,help_text='商品编号')
    name = models.CharField(max_length=255,null=True,blank=True,help_text='购买人姓名')
    profile=models.CharField(max_length=255)
    chioces = (('DE', 'DE'),('CA', 'CA'),('US', 'US'),('JP', 'JP'))
    zone=models.CharField('站点',max_length=16,choices=chioces,default='US')
    add_time=models.DateTimeField('添加时间',null=True,blank=True,editable=False)
    start_time=models.DateTimeField('执行开始时间',null=True,blank=True,editable=False)
    end_time=models.DateTimeField('执行结束时间',null=True,blank=True,editable=False)
    days=models.IntegerField('步长天数',null=True,blank=True)
    user=models.ForeignKey(User,verbose_name='创建人')

    def __str__(self):
        return self.asin
    class Meta:
        verbose_name='订单查询'
        verbose_name_plural='订单查询'

class Permission(models.Model):
    name = models.CharField("权限名称", max_length=64)
    url = models.CharField('URL名称', max_length=255)
    chioces = ((1, 'GET'), (2, 'POST'))
    per_method = models.SmallIntegerField('请求方法', choices=chioces, default=1)
    argument_list = models.CharField('参数列表', max_length=255, help_text='多个参数之间用英文半角逗号隔开', blank=True, null=True)
    describe = models.CharField('描述', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
        #权限信息，这里定义的权限的名字，后面是描述信息，描述信息是在django admin中显示权限用的
        permissions = (
            ('views_student_list', '查看学员信息表'),
            ('views_student_info', '查看学员详细信息'),
        )

class CountOfDay(models.Model):
    order_day = models.CharField("日期",max_length=64)
    total = models.IntegerField("抓取订单数量",default=0)
    success = models.IntegerField('成功获取profile数量',null=True,blank=True,editable=False)

    def __str__(self):
        return self.day
from django.db import models
from django.contrib.auth.models import User

class OrderData(models.Model):

    profile=models.CharField(max_length=255,null=True,blank=True,db_index=True,editable=False)
    chioces = (('DE', 'DE'),('CA', 'CA'),('US', 'US'),('JP', 'JP'))
    zone=models.CharField('站点',max_length=16,choices=chioces,default='US')
    order_id = models.CharField(max_length=255,db_index=True)
    order_time = models.DateTimeField('下单时间',null=True,blank=True,editable=False)
    create_time = models.DateTimeField('插入时间',null=True,blank=True,editable=False)
    update_time = models.DateTimeField('更新时间', null=True, blank=True, editable=False)
    status = models.CharField('订单状态', max_length=50, null=True, blank=True, editable=False)

    def __str__(self):
        return self.order_id
    class Meta:
        verbose_name='订单查询'
        verbose_name_plural='订单查询'


class Advise(models.Model):
    summary = models.CharField('标题',max_length=255,null=True,blank=True)
    content = models.TextField('内容',null=True,blank=True)
    user = models.ForeignKey(User, verbose_name='创建人')
    add_time = models.DateTimeField('添加时间', null=True,editable=False)
    reply = models.TextField('回复',null=True,blank=True)

    def __str__(self):
        return self.summary
    class Meta:
        verbose_name = '意见/建议'
        verbose_name_plural = '意见/建议'
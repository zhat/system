from django.db import models

class OrderData(models.Model):

    profile=models.CharField(max_length=255)
    chioces = (('DE', 'DE'),('CA', 'CA'),('US', 'US'),('JP', 'JP'))
    zone=models.CharField('站点',max_length=16,choices=chioces,default='US')
    order_id = models.CharField(max_length=255)
    order_time = models.DateTimeField('下单时间',null=True,blank=True,editable=False)
    create_time = models.DateTimeField('插入时间',null=True,blank=True,editable=False)
    update_time = models.DateTimeField('插入时间', null=True, blank=True, editable=False)

    def __str__(self):
        return self.order_id
    class Meta:
        verbose_name='订单查询'
        verbose_name_plural='订单查询'
        db_table='amazon_order_search_data'
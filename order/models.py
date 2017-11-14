from django.db import models
from django.contrib.auth.models import User


class AmazonOrderAll(models.Model):
    platform = models.CharField(max_length=32)
    channel = models.CharField(max_length=40)
    order_id = models.CharField(max_length=80)
    status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=40)
    purchase_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    amazon_updated_at = models.DateTimeField()
    lastest_ship_date = models.DateTimeField()
    lastest_delivery_date = models.DateTimeField()
    customer_name = models.CharField(max_length=40)
    email = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    currency_code = models.CharField(max_length=20, blank=True, null=True)
    country_code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    state_or_region = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=40, blank=True, null=True)
    phone = models.CharField(max_length=60, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_order'

class AmazonOrderItem(models.Model):
    parent_id = models.IntegerField()
    amazon_item_id = models.CharField(max_length=40)
    title = models.CharField(max_length=255)
    asin = models.CharField(db_column='ASIN', max_length=120)  # Field name made lowercase.
    sku = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    qty = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_discount = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    tax = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True)
    gift_price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    promotion_id = models.CharField(max_length=256, blank=True, null=True)
    promotion_discount = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    shipping_tax = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    condition_id = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    push_status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'amazon_order_item'

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

class AmazonOrder(models.Model):

    profile=models.CharField(max_length=255,null=True,blank=True,db_index=True,editable=False)
    chioces = (('DE', 'DE'),('CA', 'CA'),('US', 'US'),('JP', 'JP'))
    zone=models.CharField('站点',max_length=16,choices=chioces,default='US')
    order_id = models.CharField(max_length=255,db_index=True)
    order_time = models.DateTimeField('下单时间',null=True,blank=True,editable=False)
    create_time = models.DateTimeField('插入时间',null=True,blank=True,editable=False)
    amazon_order_id = models.IntegerField('ID', null=True, blank=True, editable=False)
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

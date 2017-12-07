from django.db import models
from datetime import datetime

# Create your models here.

class AmazonOrder(models.Model):
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
        unique_together = (('channel', 'order_id'),)


class AmazonOrderItem(models.Model):

    parent = models.ForeignKey(AmazonOrder)
    #parent_id = models.IntegerField()
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



class LightOrder(models.Model):
    entity_id = models.AutoField(primary_key=True)
    platform = models.CharField(max_length=60)
    order_id = models.CharField(max_length=50)
    light_order_id = models.CharField(max_length=50)
    state = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=4)
    subtotal = models.DecimalField(max_digits=12, decimal_places=4)
    grand_total = models.DecimalField(max_digits=12, decimal_places=4)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=4)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=4)
    total_canceled = models.DecimalField(max_digits=12, decimal_places=4)
    total_invoiced = models.DecimalField(max_digits=12, decimal_places=4)
    total_paid = models.DecimalField(max_digits=12, decimal_places=4)
    total_qty_ordered = models.DecimalField(max_digits=12, decimal_places=4)
    total_refunded = models.DecimalField(max_digits=12, decimal_places=4)
    gift_message = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=12, decimal_places=4)
    customer_email = models.CharField(max_length=255)
    customer_firstname = models.CharField(max_length=255)
    customer_lastname = models.CharField(max_length=255)
    customer_middlename = models.CharField(max_length=255)
    global_currency_code = models.CharField(max_length=3)
    order_currency_code = models.CharField(max_length=255)
    remote_ip = models.CharField(max_length=255)
    shipping_method = models.CharField(max_length=255)
    country_id = models.CharField(max_length=20)
    region_id = models.IntegerField()
    region = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    postcode = models.CharField(max_length=40)
    street = models.TextField()
    shipping_firstname = models.CharField(max_length=255)
    shipping_middlename = models.CharField(max_length=255)
    shipping_lastname = models.CharField(max_length=255)
    telephone = models.CharField(max_length=40)
    customer_note = models.TextField(blank=True, null=True)
    avs = models.CharField(max_length=4)
    payment_method = models.CharField(max_length=40)
    light_created_at = models.DateTimeField()
    paid_time = models.DateTimeField()
    light_updated_at = models.DateTimeField()
    process_status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'light_order'
        unique_together = (('platform', 'order_id'),)


class LightOrderItem(models.Model):
    entity_id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField()
    light_item_id = models.IntegerField()
    weight = models.DecimalField(max_digits=12, decimal_places=4)
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    free_shipping = models.SmallIntegerField()
    is_qty_decimal = models.SmallIntegerField()
    no_discount = models.SmallIntegerField()
    qty_canceled = models.DecimalField(max_digits=12, decimal_places=4)
    qty_invoiced = models.DecimalField(max_digits=12, decimal_places=4)
    qty_ordered = models.DecimalField(max_digits=12, decimal_places=4)
    qty_refunded = models.DecimalField(max_digits=12, decimal_places=4)
    qty_shipped = models.DecimalField(max_digits=12, decimal_places=4)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    base_price = models.DecimalField(max_digits=12, decimal_places=4)
    original_price = models.DecimalField(max_digits=12, decimal_places=4)
    tax_percent = models.DecimalField(max_digits=12, decimal_places=4)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=4)
    tax_invoiced = models.DecimalField(max_digits=12, decimal_places=4)
    discount_percent = models.DecimalField(max_digits=12, decimal_places=4)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=4)
    amount_refunded = models.DecimalField(max_digits=12, decimal_places=4)
    row_total = models.DecimalField(max_digits=12, decimal_places=4)
    gift_message_id = models.IntegerField()
    postcode = models.CharField(max_length=40)
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.TextField()
    gift_message = models.IntegerField()
    light_created_at = models.DateTimeField()
    light_updated_at = models.DateTimeField()
    ship_at = models.DateTimeField()
    push_status = models.SmallIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'light_order_item'


class EbayOrderFull(models.Model):
    id = models.BigAutoField(primary_key=True)
    account = models.CharField(max_length=50)
    order_id = models.CharField(max_length=255)
    record_number = models.BigIntegerField()
    order_status = models.CharField(max_length=50)
    adjustment_amount = models.CharField(max_length=50)
    amount_paid = models.CharField(max_length=50)
    amount_saved = models.CharField(max_length=50)
    created_time = models.DateTimeField()
    payment_methods = models.CharField(max_length=50)
    seller_email = models.CharField(max_length=255)
    sub_total = models.CharField(max_length=50)
    total = models.CharField(max_length=50)
    buyer_user_id = models.CharField(max_length=255)
    paid_time = models.DateTimeField()
    shipped_time = models.DateTimeField()
    integrated_merchant_credit_card_enabled = models.IntegerField()
    eias_token = models.CharField(max_length=255)
    payment_hold_status = models.CharField(max_length=50)
    is_multi_leg_shipping = models.IntegerField()
    seller_user_id = models.CharField(max_length=255)
    seller_eias_token = models.CharField(max_length=255, blank=True, null=True)
    cancel_status = models.CharField(max_length=50, blank=True, null=True)
    extended_order_id = models.CharField(max_length=255, blank=True, null=True)
    contains_ebay_plus_transaction = models.IntegerField(blank=True, null=True)
    checkout_status_s = models.CharField(max_length=40, blank=True, null=True)
    checkout_status = models.TextField(blank=True, null=True)
    shipping_country = models.CharField(max_length=60, blank=True, null=True)
    shipping_region = models.CharField(max_length=60, blank=True, null=True)
    shipping_postcode = models.CharField(max_length=40, blank=True, null=True)
    shipping_details = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    shipping_service_selected = models.TextField(blank=True, null=True)
    external_transaction = models.TextField(blank=True, null=True)
    transaction_array = models.TextField(blank=True, null=True)
    monetary_details = models.TextField(blank=True, null=True)
    last_modified_time = models.DateTimeField()
    last_fetch_time = models.DateTimeField()
    has_pushed = models.IntegerField()
    process_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ebay_order_full'


class EbayOrderFullItem(models.Model):
    order_id = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255)
    transaction_site_id = models.CharField(max_length=50)
    email = models.CharField(max_length=80, blank=True, null=True)
    item_id = models.CharField(max_length=255, blank=True, null=True)
    item_sku = models.CharField(max_length=50, blank=True, null=True)
    item_title = models.CharField(max_length=50, blank=True, null=True)
    quantity_purchased = models.CharField(max_length=50, blank=True, null=True)
    transaction_price = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ebay_order_full_item'


class StatisticsData(models.Model):
    date = models.DateField("日期")
    sku=models.CharField("sku",max_length=128, null=True)
    asin=models.CharField("asin",max_length=128, null=True)
    platform=models.CharField("账号",max_length=32, null=True)
    station=models.CharField("站点",max_length=64, null=True)
    qty=models.IntegerField("订单数量", null=True)
    currencycode=models.CharField("币种",max_length=32, null=True)
    deduction=models.FloatField("折扣额", null=True)
    price=models.FloatField("金额", null=True)
    count=models.IntegerField("总数",null=True)
    sametermrate=models.FloatField("同比",null=True)
    weekrate=models.FloatField("周环比",null=True)
    monthrate=models.FloatField("月环比",null=True)
    status=models.CharField("订单状态",max_length=32,null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    #create_time = models.DateTimeField(auto_now_add=True,default=datetime.now(),null=True)

    def __str__(self):
        return str(self.date)+self.asin

    class Meta:
        verbose_name = "单品每日统计临时表"
        verbose_name_plural = "单品每日统计临时表"

class StatisticsOfPlatform(models.Model):
    date = models.DateField("日期")
    platform = models.CharField("账号", max_length=32, null=True)
    station = models.CharField("站点", max_length=64, null=True)
    qty = models.IntegerField("订单数量", null=True)
    count = models.IntegerField("总数", null=True)
    currencycode = models.CharField("币种", max_length=32, null=True)
    site_price = models.FloatField("站点金额", null=True)
    dollar_price = models.FloatField("美元金额",null=True)
    RMB_price = models.FloatField("人民币金额",null=True)
    sametermrate = models.FloatField("同比", null=True)
    weekrate = models.FloatField("周环比", null=True)
    monthrate = models.FloatField("月环比", null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    #create_time = models.DateTimeField(auto_now_add=True,default=datetime.now(),null=True)

    def __str__(self):
        return str(self.date)+self.station

    class Meta:
        verbose_name = "站点每日总计"
        verbose_name_plural = "站点每日总计"
        ordering = ['-date']


class AsinInfo(models.Model):
    date = models.DateField("日期")
    sku = models.CharField("sku", max_length=128, null=True)
    asin = models.CharField("asin", max_length=128, null=True)
    platform = models.CharField("账号", max_length=32, null=True)
    station = models.CharField("站点", max_length=64, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    #create_time = models.DateTimeField(auto_now_add=True,default=datetime.now(),null=True)

    def __str__(self):
        return self.asin

    class Meta:
        verbose_name = "每日asin信息"
        verbose_name_plural = "每日asin信息"

class ReportData(models.Model):

    date = models.DateField("日期")
    sku = models.CharField("sku", max_length=128, null=True)
    asin = models.CharField("asin", max_length=128, null=True)
    platform = models.CharField("账号", max_length=32, null=True)
    station = models.CharField("站点", max_length=64, null=True)
    qty = models.IntegerField("订单数量", null=True)
    currencycode = models.CharField("币种", max_length=32, null=True)
    deduction = models.FloatField("折扣额", null=True)
    price = models.FloatField("金额", null=True)
    count = models.IntegerField("总数", null=True)
    sametermrate = models.FloatField("同比", null=True)
    weekrate = models.FloatField("周环比", null=True)
    monthrate = models.FloatField("月环比", null=True)
    status = models.CharField("订单状态", max_length=32, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    #create_time = models.DateTimeField(auto_now_add=True,default=datetime.now(),null=True)
    #update_time = models.DateTimeField(auto_now=True,default=datetime.now(),null=True)

    def __str__(self):
        return str(self.date) + self.asin

    class Meta:
        verbose_name = "单品每日统计结果表"
        verbose_name_plural = "单品每日统计结果表"

class ProductStock(models.Model):
    date = models.DateField("日期")
    sku = models.CharField("sku", max_length=128, null=True)
    asin = models.CharField("asin", max_length=128, null=True)
    platform = models.CharField("账号", max_length=32, null=True)
    station = models.CharField("站点", max_length=64, null=True)
    stock = models.IntegerField("库存数",null=True)
    quantity = models.IntegerField(null= True)
    reserved = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sku
    class Meta:
        verbose_name = "库存信息表"
        verbose_name_plural = "库存信息表"

class AmazonProductBaseinfo(models.Model):
    zone = models.CharField(max_length=8, blank=True, null=True)
    asin = models.CharField(max_length=20, blank=True, null=True)
    ref_id = models.CharField(max_length=20, blank=True, null=True)
    seller_name = models.CharField(max_length=50, blank=True, null=True)
    seller_url = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    brand_url = models.CharField(max_length=100, blank=True, null=True)
    is_fba = models.CharField(max_length=2, blank=True, null=True)
    stock_situation = models.CharField(max_length=50, blank=True, null=True)
    category_name = models.CharField(max_length=255, blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    in_sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    review_cnt = models.IntegerField(blank=True, null=True)
    review_avg_star = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percent_5_star = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percent_4_star = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percent_3_star = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percent_2_star = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    percent_1_star = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cnt_qa = models.IntegerField(blank=True, null=True)
    offers_url = models.CharField(max_length=200, blank=True, null=True)
    lowest_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_product_baseinfo'

class CompetitiveProduct(models.Model):
    """info = {'sku': sku, 'score': score, 'comments': comments, 'zone': zone, 'asin': asin,
            'competitive_product_asin': competitive_product_asin,
            'competitive_product_score': competitive_product_score,
            'competitive_product_comments': competitive_product_comments}"""
    zone = models.CharField(max_length=63, blank=True, null=True)
    asin = models.CharField(max_length=63, blank=True, null=True)
    sku = models.CharField(max_length=63,blank=True, null=True)
    score = models.CharField(max_length=63, blank=True, null=True)
    comments = models.CharField(max_length=63, blank=True, null=True)
    competitive_product_asin = models.CharField(max_length=63, blank=True, null=True)
    competitive_product_score = models.CharField(max_length=63, blank=True, null=True)
    competitive_product_comments = models.CharField(max_length=63, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True,blank=True, null=True)


class AmazonBusinessReport(models.Model):
    zone = models.CharField(max_length=10, blank=True, null=True)
    sub_zone = models.CharField(max_length=10, blank=True, null=True)
    data_date = models.CharField(max_length=50, blank=True, null=True)
    parent_asin = models.CharField(max_length=50, blank=True, null=True)
    child_asin = models.CharField(max_length=50, blank=True, null=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    sessions = models.IntegerField(blank=True, null=True)
    session_percentage = models.CharField(max_length=20, blank=True, null=True)
    page_views = models.IntegerField(blank=True, null=True)
    page_view_percentage = models.CharField(max_length=20, blank=True, null=True)
    buy_box = models.CharField(max_length=20, blank=True, null=True)
    units_ordered = models.IntegerField(blank=True, null=True)
    units_ordered_b2b = models.IntegerField(blank=True, null=True)
    unit_session_percentage = models.CharField(max_length=20, blank=True, null=True)
    unit_session_percentage_b2b = models.CharField(max_length=20, blank=True, null=True)
    ordered_product_sales = models.FloatField(blank=True, null=True)
    ordered_product_sales_b2b = models.FloatField(blank=True, null=True)
    total_order_items = models.IntegerField(blank=True, null=True)
    total_order_items_b2b = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_business_report'


class AmazonTodayDeal(models.Model):
    date = models.CharField(max_length=32)
    zone = models.CharField(max_length=8, blank=True, null=True)
    asin = models.CharField(max_length=31, blank=True, null=True)
    page = models.IntegerField(blank=True, null=True)
    page_index = models.IntegerField(blank=True, null=True)
    deal_url = models.TextField(blank=True, null=True)
    deal_type = models.CharField(max_length=127, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_today_deal'

class AmazonDailyInventory(models.Model):
    sku = models.CharField(max_length=50, blank=True, null=True)
    fnsku = models.CharField(max_length=50, blank=True, null=True)
    asin = models.CharField(max_length=50, blank=True, null=True)
    afn_fulfillable_quantity = models.IntegerField(blank=True, null=True)
    zone = models.CharField(max_length=20, blank=True, null=True)
    sub_zone = models.CharField(max_length=20, blank=True, null=True)
    data_date = models.CharField(max_length=20, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_daily_inventory'

class ProductInfo(models.Model):
    date = models.DateField("日期")
    zone = models.CharField(max_length=20, blank=True, null=True)
    sku = models.CharField(max_length=128, blank=True, null=True)
    asin = models.CharField(max_length=128, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return self.asin
    class Meta:
        verbose_name = "商品信息"
        verbose_name_plural = "商品信息"

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


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
    is_system = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_order'
        unique_together = (('channel', 'order_id'),)


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


class AmazonOrderSearchData(models.Model):
    profile = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50)
    order_time = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'amazon_order_search_data'


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


class AmazonProductReviews(models.Model):
    zone = models.CharField(max_length=8, blank=True, null=True)
    asin = models.CharField(max_length=20, blank=True, null=True)
    ref_id = models.CharField(max_length=20, blank=True, null=True)
    review_url = models.CharField(max_length=255, blank=True, null=True)
    review_id = models.CharField(max_length=50, blank=True, null=True)
    review_title = models.CharField(max_length=255, blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)
    reviewer_name = models.CharField(max_length=255, blank=True, null=True)
    reviewer_url = models.CharField(max_length=255, blank=True, null=True)
    review_date = models.CharField(max_length=30, blank=True, null=True)
    item_package_quantity = models.IntegerField()
    item_color_size_info = models.CharField(max_length=20, blank=True, null=True)
    order_index = models.IntegerField(blank=True, null=True)
    review_star = models.CharField(max_length=20, blank=True, null=True)
    is_verified_purchase = models.CharField(max_length=4, blank=True, null=True)
    votes = models.CharField(max_length=20, blank=True, null=True)
    comments = models.CharField(max_length=20, blank=True, null=True)
    top_reviewer_info = models.CharField(max_length=50, blank=True, null=True)
    cnt_imgs = models.IntegerField(blank=True, null=True)
    cnt_vedios = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_product_reviews'


class AmazonRefShopList(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    shop_name = models.CharField(max_length=50, blank=True, null=True)
    shop_url = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=8, blank=True, null=True)
    brand = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=40, blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_ref_shop_list'


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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CeleryTaskmeta(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    hidden = models.IntegerField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'celery_taskmeta'


class CeleryTasksetmeta(models.Model):
    taskset_id = models.CharField(unique=True, max_length=255)
    result = models.TextField()
    date_done = models.DateTimeField()
    hidden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'celery_tasksetmeta'


class CoreAmazonAccount(models.Model):
    platform = models.CharField(max_length=40)
    department = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=40)
    password_encrypt = models.CharField(max_length=100)
    login_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'core_amazon_account'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    hidden = models.IntegerField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjceleryCrontabschedule(models.Model):
    minute = models.CharField(max_length=64)
    hour = models.CharField(max_length=64)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=64)
    month_of_year = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'djcelery_crontabschedule'


class DjceleryIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'djcelery_intervalschedule'


class DjceleryPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.IntegerField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.IntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjceleryCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjceleryIntervalschedule, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_periodictask'


class DjceleryPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'djcelery_periodictasks'


class DjceleryTaskstate(models.Model):
    state = models.CharField(max_length=64)
    task_id = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=200, blank=True, null=True)
    tstamp = models.DateTimeField()
    args = models.TextField(blank=True, null=True)
    kwargs = models.TextField(blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)
    runtime = models.FloatField(blank=True, null=True)
    retries = models.IntegerField()
    hidden = models.IntegerField()
    worker = models.ForeignKey('DjceleryWorkerstate', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_taskstate'


class DjceleryWorkerstate(models.Model):
    hostname = models.CharField(unique=True, max_length=255)
    last_heartbeat = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djcelery_workerstate'


class DjkombuMessage(models.Model):
    visible = models.IntegerField()
    sent_at = models.DateTimeField(blank=True, null=True)
    payload = models.TextField()
    queue = models.ForeignKey('DjkombuQueue', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djkombu_message'


class DjkombuQueue(models.Model):
    name = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'djkombu_queue'


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


class Feedback(models.Model):
    date = models.DateField()
    shop_name = models.CharField(max_length=64, blank=True, null=True)
    last_30_days = models.IntegerField(blank=True, null=True)
    last_90_days = models.IntegerField(blank=True, null=True)
    last_12_months = models.IntegerField(blank=True, null=True)
    lifetime = models.IntegerField(blank=True, null=True)
    last_day = models.IntegerField(blank=True, null=True)
    last_week = models.IntegerField(blank=True, null=True)
    last_month = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    zone = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback'


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


class MonitorFeedback(models.Model):
    date = models.DateField()
    store = models.CharField(max_length=64, blank=True, null=True)
    last_30_days = models.IntegerField(blank=True, null=True)
    last_90_days = models.IntegerField(blank=True, null=True)
    last_12_months = models.IntegerField(blank=True, null=True)
    lifetime = models.IntegerField(blank=True, null=True)
    last_day = models.IntegerField(blank=True, null=True)
    last_week = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    station = models.ForeignKey('MonitorStation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'monitor_feedback'


class MonitorStation(models.Model):
    platform = models.CharField(max_length=32, blank=True, null=True)
    station = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitor_station'


class OrderAdvise(models.Model):
    summary = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    add_time = models.DateTimeField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'order_advise'


class OrderAmazonorder(models.Model):
    profile = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=16)
    order_id = models.CharField(max_length=255)
    order_time = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    amazon_order_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_amazonorder'


class OrderOrderdata(models.Model):
    profile = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=16)
    order_id = models.CharField(max_length=255)
    order_time = models.DateTimeField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_orderdata'


class ReportAsininfo(models.Model):
    date = models.DateField()
    sku = models.CharField(max_length=128, blank=True, null=True)
    asin = models.CharField(max_length=128, blank=True, null=True)
    platform = models.CharField(max_length=32, blank=True, null=True)
    station = models.CharField(max_length=64, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_asininfo'


class ReportCompetitiveproduct(models.Model):
    zone = models.CharField(max_length=63, blank=True, null=True)
    asin = models.CharField(max_length=63, blank=True, null=True)
    sku = models.CharField(max_length=63, blank=True, null=True)
    score = models.CharField(max_length=63, blank=True, null=True)
    comments = models.CharField(max_length=63, blank=True, null=True)
    competitive_product_asin = models.CharField(max_length=63, blank=True, null=True)
    competitive_product_score = models.CharField(max_length=63, blank=True, null=True)
    competitive_product_comments = models.CharField(max_length=63, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_competitiveproduct'


class ReportProductinfo(models.Model):
    date = models.DateField()
    zone = models.CharField(max_length=20, blank=True, null=True)
    sku = models.CharField(max_length=128, blank=True, null=True)
    asin = models.CharField(max_length=128, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_productinfo'


class ReportProductstock(models.Model):
    date = models.DateField()
    sku = models.CharField(max_length=128, blank=True, null=True)
    asin = models.CharField(max_length=128, blank=True, null=True)
    platform = models.CharField(max_length=32, blank=True, null=True)
    station = models.CharField(max_length=64, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    reserved = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_productstock'


class ReportReportdata(models.Model):
    date = models.DateField()
    sku = models.CharField(max_length=128, blank=True, null=True)
    asin = models.CharField(max_length=128, blank=True, null=True)
    platform = models.CharField(max_length=32, blank=True, null=True)
    station = models.CharField(max_length=64, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    currencycode = models.CharField(max_length=32, blank=True, null=True)
    deduction = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    sametermrate = models.FloatField(blank=True, null=True)
    weekrate = models.FloatField(blank=True, null=True)
    monthrate = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_reportdata'


class ReportStatisticsdata(models.Model):
    date = models.DateField()
    sku = models.CharField(max_length=128, blank=True, null=True)
    asin = models.CharField(max_length=128, blank=True, null=True)
    platform = models.CharField(max_length=32, blank=True, null=True)
    station = models.CharField(max_length=64, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    currencycode = models.CharField(max_length=32, blank=True, null=True)
    deduction = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    sametermrate = models.FloatField(blank=True, null=True)
    weekrate = models.FloatField(blank=True, null=True)
    monthrate = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_statisticsdata'


class ReportStatisticsofplatform(models.Model):
    date = models.DateField()
    platform = models.CharField(max_length=32, blank=True, null=True)
    station = models.CharField(max_length=64, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    currencycode = models.CharField(max_length=32, blank=True, null=True)
    site_price = models.FloatField(blank=True, null=True)
    dollar_price = models.FloatField(blank=True, null=True)
    rmb_price = models.FloatField(db_column='RMB_price', blank=True, null=True)  # Field name made lowercase.
    sametermrate = models.FloatField(blank=True, null=True)
    weekrate = models.FloatField(blank=True, null=True)
    monthrate = models.FloatField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_statisticsofplatform'


class SpiderCountofday(models.Model):
    order_day = models.CharField(max_length=64)
    total = models.IntegerField()
    success = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spider_countofday'


class SpiderOrdercrawl(models.Model):
    asin = models.CharField(max_length=255)
    zone = models.CharField(max_length=16)
    add_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    profile = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spider_ordercrawl'


class SpiderPermission(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255)
    per_method = models.SmallIntegerField()
    argument_list = models.CharField(max_length=255, blank=True, null=True)
    describe = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'spider_permission'

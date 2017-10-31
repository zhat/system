from django.contrib import admin

# Register your models here.
from .models import OrderCrawl

class OrderCrawlAdmin(admin.ModelAdmin):
    list_display = ('asin','name','profile','zone','add_time','start_time','end_time','days','user')

admin.site.register(OrderCrawl,OrderCrawlAdmin)
from django.contrib import admin

# Register your models here.
from .models import Permission,Student,OrderCrawl

admin.site.register(Permission)
admin.site.register(OrderCrawl)
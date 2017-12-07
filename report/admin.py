from django.contrib import admin

# Register your models here.
from .models import StatisticsData,StatisticsOfPlatform,ReportData,ProductStock,ProductInfo

class StatisticsDataAdmin(admin.ModelAdmin):
    list_display = ('date','sku','asin','platform','station','qty','currencycode','deduction','price',
                    'count','sametermrate','weekrate','monthrate','status')
class ReportDataAdmin(admin.ModelAdmin):
    list_display = ('date','sku','asin','platform','station','qty','currencycode','deduction','price',
                    'count','sametermrate','weekrate','monthrate','status')

class StatisticsOfPlatformAdmin(admin.ModelAdmin):
    list_display = ('date','platform','station','qty','count','currencycode','site_price',
                    'dollar_price','RMB_price','sametermrate','weekrate','monthrate')

class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('date','sku','asin','platform','station','stock','create_time')

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('date','zone','asin','sku','create_time')

admin.site.register(StatisticsData,StatisticsDataAdmin)
admin.site.register(StatisticsOfPlatform,StatisticsOfPlatformAdmin)
admin.site.register(ReportData,ReportDataAdmin)
admin.site.register(ProductStock,ProductStockAdmin)
admin.site.register(ProductInfo,ProductInfoAdmin)
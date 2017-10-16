from django.contrib import admin
from .models import Station,Feedback
# Register your models here.

class StationAdmin(admin.ModelAdmin):
    list_display = ('platform','station')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('date','station','store','last_30_days','last_90_days','last_12_months',
                    'lifetime','last_day','last_week','create_time','update_time')

admin.site.register(Station,StationAdmin)
admin.site.register(Feedback,FeedbackAdmin)

from django.contrib import admin
from .models import OrderData,Advise
# Register your models here.
from django.contrib.auth.models import Permission

admin.site.register(Permission)
admin.site.register(Advise)
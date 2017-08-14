from django.shortcuts import render
from .models import OrderData
# Create your views here.

def search(request):
    order=OrderData.objects.first()

    return render(request,'order/index.html',{'order':order})
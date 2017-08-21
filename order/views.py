from django.shortcuts import render
from datetime import datetime
from .models import OrderData,Advise
from django.contrib.auth.decorators import login_required
from .forms import AdviseForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.
@login_required
def search(request):
    try:
        profile = request.GET['profile']
    except Exception as e:
        print(e)
        profile=""
    print(profile)
    profile=profile.strip()
    if profile:
        try:
            order = OrderData.objects.get(profile__contains=profile)
            result = 1
        except Exception as e:
            print(e)
            result = 2
            order = '没有查询到订单信息'
        return render(request,'order/index.html',{'result':result,'order':order})
    else:
        return render(request, 'order/index.html',{'result':0})


@login_required
def add_advise(request):
    if request.method=="POST":
        form = AdviseForm(request.POST)
        if form.is_valid():
            new_advise = form.save(commit=False)
            new_advise.add_time= datetime.now()
            new_advise.user=request.user
            new_advise.save()
            return HttpResponseRedirect(reverse('order:search'))
    else:
        return render(request,'order/add_advise.html')
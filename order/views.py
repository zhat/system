from django.shortcuts import render
from datetime import datetime
from .models import OrderData,Advise
from django.contrib.auth.decorators import login_required
from .forms import AdviseForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        order_list = OrderData.objects.filter(profile__contains=profile).all().order_by('-order_time')
        paginator = Paginator(order_list, 10)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            order_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            order_list = paginator.page(1)
        result = 1
        return render(request,'order/index.html',{'order_list':order_list,'profile':profile})
    else:
        return render(request, 'order/index.html',{})

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
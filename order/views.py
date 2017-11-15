from django.shortcuts import render
from datetime import datetime
from .models import OrderData, AmazonOrderRemote,AmazonOrderItemRemote
from django.contrib.auth.decorators import login_required
from .forms import AdviseForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
# Create your views here.


@login_required
def search_by_profile(request):
    profile = request.GET.get('profile', '').strip()
    if profile:
        order_list = OrderData.objects.filter(
            profile=profile).all().order_by('-order_time')
        paginator = Paginator(order_list, 10)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            order_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            order_list = paginator.page(1)
        return render(request, 'order/search_by_profile.html',{'order_list': order_list, 'profile': profile})
    else:
        return render(request, 'order/search_by_profile.html', {})

@login_required
def search_by_name(request):
    name = request.GET.get('name', '').strip()
    zone = request.GET.get('zone', '').strip()
    asin = request.GET.get('asin', '').strip()
    print(name)
    order_of_name = []
    if name and zone:
        print(datetime.now())
        order_list = AmazonOrderRemote.objects.using('remote').filter(platform=zone).\
            filter(customer_name__iexact=name).all()
        # if asin:
        #     order_id_list =[order.id for order in order_list]
        #     if order_id_list:
        #         order_items = AmazonOrderItem.objects.filter(zone=zone).\
        #             filter(asin=asin).\
        #             filter(parent_id__in=order_id_list).all()
        for order in order_list:
            order_items = AmazonOrderItemRemote.objects.using('remote'). \
                         filter(parent_id=order.id).all()
            order_item_asin_list = [order_item.asin for order_item in order_items]
            order_dict = {
                'zone': order.platform,
                'order_id': order.order_id,
                'order_time': order.purchase_at,
                'customer_name':order.customer_name,
                'asin_list':','.join(order_item_asin_list)
            }
            order_of_name.append(order_dict)
        print(datetime.now())
        return render(request, 'order/search_by_name.html',
                      {'order_of_name':order_of_name,'name':name,'zone':zone,'asin':asin})
    else:
        return render(request, 'order/search_by_name.html', {})

@login_required
def search_by_name_and_profile(request):
    profile = request.GET.get('profile', '').strip()
    name = request.GET.get('name', '').strip()
    zone = request.GET.get('zone', '').strip()
    asin = request.GET.get('asin', '').strip()
    order_of_name = []
    if name and zone:
        order_list = AmazonOrderRemote.objects.filter(platform=zone).\
            filter(customer_name__iexact=name).all()
        # if asin:
        #     order_id_list =[order.id for order in order_list]
        #     if order_id_list:
        #         order_items = AmazonOrderItem.objects.filter(zone=zone).\
        #             filter(asin=asin).\
        #             filter(parent_id__in=order_id_list).all()
        for order in order_list:
            order_items = AmazonOrderItemRemote.objects. \
                         filter(parent_id=order.id).all()
            order_item_asin_list = [order_item.asin for order_item in order_items]
            order_dict = {
                'zone': order.platform,
                'order_id': order.order_id,
                'order_time': order.purchase_at,
                'customer_name':order.customer_name,
                'asin_list':','.join(order_item_asin_list)
            }
            order_of_name.append(order_dict)

    if profile:
        order_list = OrderData.objects.filter(
            profile=profile).all().order_by('-order_time')
        paginator = Paginator(order_list, 10)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            order_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            order_list = paginator.page(1)
        return render(request, 'order/search_by_name_and_profile.html',
                      {'order_list': order_list, 'order_of_name':order_of_name,
                       'profile': profile,'name':name,'zone':zone,'asin':asin})
    else:
        return render(request, 'order/search_by_name_and_profile.html', {})


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
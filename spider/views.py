from datetime import datetime
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from .models import Student,OrderCrawl
from .permission import  check_permission
from .forms import OrderCrawlForm
from .tasks import get_order_info,add
# Create your views here.

@check_permission
def students(request):
    students_obj = Student.objects.all()
    return render(request, 'students_list.html', locals())

def index(request):
    return render(request, 'spider/index.html', {})
@login_required
def orders(request):
    order_list = OrderCrawl.objects.all().order_by('-add_time')
    paginator = Paginator(order_list, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        order_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        order_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        order_list = paginator.page(paginator.num_pages)
    return render(request,'spider/list.html',{'order_list':order_list})

@login_required
def order_add(request):
    if request.method=='POST':
        form=OrderCrawlForm(request.POST)
        print(request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.add_time = datetime.now()
            new_order.save()
            get_order_info.delay(new_order.id)
    return HttpResponseRedirect(reverse('spider:orders'))

def task_demo(request):
    order=OrderCrawl.objects.first()
    print(order.id)
    get_order_info.delay(order.id)
    return render(request,'spider/list.html',{})
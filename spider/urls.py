from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'index/$',views.index,name='index'),
    url(r'list/$',views.orders,name='orders'),
    url(r'add/$',views.order_add,name='add'),
    url(r'students/$', views.students, name='students_list'),
    url(r'task_demo/$',views.task_demo,name='task_demo'),
]
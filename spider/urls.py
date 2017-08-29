from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'list/$',views.orders,name='orders'),
    url(r'add/$',views.order_add,name='add'),
    url(r'count/$',views.count,name='count'),
]
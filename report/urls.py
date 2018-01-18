from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'test/$',views.date_test,name='test'),
    url(r'product_list/$',views.product_list,name="product_list"),
    url(r'product_detail/$',views.product_detail,name="product_detail"),
    url(r'product_data/$',views.product_detail_date,name="product_detail_date"),
    url(r'data/$',views.get_data,name='get_data'),
    url(r'^$',views.index,name='index'),
]
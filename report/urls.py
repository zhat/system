from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'test$',views.date_test,name='test'),
    url(r'product_list$',views.product_list,name="product_list"),
    url(r'product/(?P<asin>\w+)/$',views.product_detail,name="product_detail"),
    url(r'^$',views.index,name='index'),
]
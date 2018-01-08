from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'feedback/$',views.feedback,name='feedback'),
    url(r'feedback_week/$',views.feedback_week,name='feedback_week'),
    url(r'review_counts/$',views.review_counts,name='review_counts'),
    url(r'review_of_asin_detail/$',views.review_of_asin_detail,name='review_of_asin_detail'),
    url(r'review_of_asin/$',views.review_of_asin,name='review_of_asin'),
    url(r'review_of_zone/$',views.review_of_zone,name='review_of_zone'),
]
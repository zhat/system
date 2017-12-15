from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'feedback/$',views.feedback,name='feedback'),
    url(r'feedback_week/$',views.feedback_week,name='feedback_week'),
    url(r'review_counts/$',views.review_counts,name='review_counts'),
    url(r'review_count_with_asin/$',views.review_count_with_asin,name='review_count_with_asin'),
]
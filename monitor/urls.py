from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'feedback/$',views.feedback,name='feedback'),
    url(r'feedback_week/$',views.feedback_week,name='feedback_week'),
]
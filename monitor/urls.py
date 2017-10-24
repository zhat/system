from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'feedback/$',views.feedback,name='feedback'),
    url(r'send_email/$',views.send_email_web,name="send_email"),
]